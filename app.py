from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import qrcode
import io
import base64
from datetime import datetime, timedelta
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/qr_codes'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('parking.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  vehicle_no TEXT UNIQUE NOT NULL,
                  qr_code TEXT UNIQUE NOT NULL,
                  phone TEXT,
                  email TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Slots table
    c.execute('''CREATE TABLE IF NOT EXISTS slots
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  slot_number TEXT UNIQUE NOT NULL,
                  status TEXT DEFAULT 'available',
                  vehicle_no TEXT,
                  entry_time TIMESTAMP,
                  qr_code TEXT)''')
    
    # Parking logs table
    c.execute('''CREATE TABLE IF NOT EXISTS parking_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  vehicle_no TEXT NOT NULL,
                  slot_id INTEGER,
                  qr_code TEXT,
                  entry_time TIMESTAMP NOT NULL,
                  exit_time TIMESTAMP,
                  duration_minutes INTEGER,
                  fee REAL DEFAULT 0,
                  status TEXT DEFAULT 'active',
                  FOREIGN KEY (user_id) REFERENCES users(id),
                  FOREIGN KEY (slot_id) REFERENCES slots(id))''')
    
    # Initialize slots if empty
    c.execute('SELECT COUNT(*) FROM slots')
    if c.fetchone()[0] == 0:
        for i in range(1, 51):  # 50 slots
            c.execute('INSERT INTO slots (slot_number, status) VALUES (?, ?)', 
                     (f'SLOT-{i:03d}', 'available'))
    
    conn.commit()
    conn.close()

# Helper functions
def get_db_connection():
    conn = sqlite3.connect('parking.db')
    conn.row_factory = sqlite3.Row
    return conn

def calculate_fee(entry_time, exit_time):
    """Calculate parking fee based on time"""
    if not exit_time:
        exit_time = datetime.now()
    
    if isinstance(entry_time, str):
        entry_time = datetime.fromisoformat(entry_time)
    if isinstance(exit_time, str):
        exit_time = datetime.fromisoformat(exit_time)
    
    duration = exit_time - entry_time
    total_minutes = int(duration.total_seconds() / 60)
    
    if total_minutes <= 30:
        return 20.0
    else:
        extra_30min_blocks = (total_minutes - 30 + 29) // 30  # Ceiling division
        return 20.0 + (extra_30min_blocks * 10.0)

def generate_qr_code(data):
    """Generate QR code image"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entry')
def entry():
    return render_template('entry.html')

@app.route('/exit')
def exit_page():
    return render_template('exit.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/register')
def register():
    return render_template('register.html')

# API Routes
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name')
    vehicle_no = data.get('vehicle_no')
    phone = data.get('phone', '')
    email = data.get('email', '')
    
    if not name or not vehicle_no:
        return jsonify({'error': 'Name and vehicle number are required'}), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if vehicle already exists
    c.execute('SELECT * FROM users WHERE vehicle_no = ?', (vehicle_no,))
    if c.fetchone():
        conn.close()
        return jsonify({'error': 'Vehicle already registered'}), 400
    
    # Generate QR code
    qr_data = f"PARKING:{vehicle_no}:{datetime.now().timestamp()}"
    qr_code = base64.b64encode(qr_data.encode()).decode()[:20]
    
    # Insert user
    c.execute('''INSERT INTO users (name, vehicle_no, qr_code, phone, email)
                 VALUES (?, ?, ?, ?, ?)''',
              (name, vehicle_no, qr_code, phone, email))
    user_id = c.lastrowid
    
    conn.commit()
    conn.close()
    
    # Generate QR image
    qr_image = generate_qr_code(qr_data)
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'qr_code': qr_code,
        'qr_image': qr_image,
        'qr_data': qr_data
    })

@app.route('/api/entry', methods=['POST'])
def api_entry():
    data = request.json
    qr_data = data.get('qr_data')
    
    if not qr_data:
        return jsonify({'error': 'QR code data required'}), 400
    
    # Parse QR data
    try:
        parts = qr_data.split(':')
        if len(parts) < 2 or parts[0] != 'PARKING':
            return jsonify({'error': 'Invalid QR code'}), 400
        vehicle_no = parts[1]
    except:
        return jsonify({'error': 'Invalid QR code format'}), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get user
    c.execute('SELECT * FROM users WHERE vehicle_no = ?', (vehicle_no,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'Vehicle not registered'}), 404
    
    # Check if already parked
    c.execute('''SELECT * FROM parking_logs 
                 WHERE vehicle_no = ? AND status = 'active' ''', (vehicle_no,))
    active_log = c.fetchone()
    if active_log:
        conn.close()
        return jsonify({'error': 'Vehicle already parked'}), 400
    
    # Find available slot
    c.execute('SELECT * FROM slots WHERE status = ? LIMIT 1', ('available',))
    slot = c.fetchone()
    if not slot:
        conn.close()
        return jsonify({'error': 'No slots available'}), 400
    
    # Assign slot
    entry_time = datetime.now()
    c.execute('''UPDATE slots SET status = ?, vehicle_no = ?, 
                 entry_time = ?, qr_code = ? WHERE id = ?''',
              ('occupied', vehicle_no, entry_time, user['qr_code'], slot['id']))
    
    # Create parking log
    c.execute('''INSERT INTO parking_logs 
                 (user_id, vehicle_no, slot_id, qr_code, entry_time, status)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (user['id'], vehicle_no, slot['id'], user['qr_code'], entry_time, 'active'))
    log_id = c.lastrowid
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'slot_number': slot['slot_number'],
        'entry_time': entry_time.isoformat(),
        'log_id': log_id
    })

@app.route('/api/exit', methods=['POST'])
def api_exit():
    data = request.json
    qr_data = data.get('qr_data')
    
    if not qr_data:
        return jsonify({'error': 'QR code data required'}), 400
    
    # Parse QR data
    try:
        parts = qr_data.split(':')
        if len(parts) < 2 or parts[0] != 'PARKING':
            return jsonify({'error': 'Invalid QR code'}), 400
        vehicle_no = parts[1]
    except:
        return jsonify({'error': 'Invalid QR code format'}), 400
    
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get active parking log
    c.execute('''SELECT pl.*, s.slot_number FROM parking_logs pl
                 JOIN slots s ON pl.slot_id = s.id
                 WHERE pl.vehicle_no = ? AND pl.status = 'active' ''', (vehicle_no,))
    log = c.fetchone()
    
    if not log:
        conn.close()
        return jsonify({'error': 'No active parking found'}), 404
    
    # Calculate fee
    exit_time = datetime.now()
    entry_time = datetime.fromisoformat(log['entry_time'])
    duration = exit_time - entry_time
    duration_minutes = int(duration.total_seconds() / 60)
    fee = calculate_fee(entry_time, exit_time)
    
    # Update parking log
    c.execute('''UPDATE parking_logs 
                 SET exit_time = ?, duration_minutes = ?, fee = ?, status = 'completed'
                 WHERE id = ?''',
              (exit_time, duration_minutes, fee, log['id']))
    
    # Free the slot
    c.execute('UPDATE slots SET status = ?, vehicle_no = NULL, entry_time = NULL, qr_code = NULL WHERE id = ?',
              ('available', log['slot_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'slot_number': log['slot_number'],
        'entry_time': log['entry_time'],
        'exit_time': exit_time.isoformat(),
        'duration_minutes': duration_minutes,
        'fee': fee
    })

@app.route('/api/slots')
def api_slots():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM slots ORDER BY slot_number')
    slots = [dict(row) for row in c.fetchall()]
    
    available = sum(1 for s in slots if s['status'] == 'available')
    occupied = sum(1 for s in slots if s['status'] == 'occupied')
    
    conn.close()
    
    return jsonify({
        'slots': slots,
        'stats': {
            'total': len(slots),
            'available': available,
            'occupied': occupied
        }
    })

@app.route('/api/users')
def api_users():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM users ORDER BY created_at DESC')
    users = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify({'users': users})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check if user exists
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user has active parking
    c.execute('SELECT * FROM parking_logs WHERE user_id = ? AND status = ?', (user_id, 'active'))
    active_parking = c.fetchone()
    if active_parking:
        conn.close()
        return jsonify({'error': 'Cannot delete user with active parking. Please process exit first.'}), 400
    
    # Delete user
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'User deleted successfully'})

@app.route('/api/logs')
def api_logs():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''SELECT pl.*, u.name, s.slot_number 
                 FROM parking_logs pl
                 LEFT JOIN users u ON pl.user_id = u.id
                 LEFT JOIN slots s ON pl.slot_id = s.id
                 ORDER BY pl.entry_time DESC LIMIT 100''')
    logs = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify({'logs': logs})

@app.route('/api/stats')
def api_stats():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Total revenue
    c.execute('SELECT SUM(fee) as total_revenue FROM parking_logs WHERE status = "completed"')
    total_revenue = c.fetchone()['total_revenue'] or 0
    
    # Today's revenue
    today = datetime.now().date()
    c.execute('''SELECT SUM(fee) as today_revenue FROM parking_logs 
                 WHERE status = "completed" AND DATE(exit_time) = ?''', (today,))
    today_revenue = c.fetchone()['today_revenue'] or 0
    
    # Active parkings
    c.execute('SELECT COUNT(*) as active FROM parking_logs WHERE status = "active"')
    active_parkings = c.fetchone()['active']
    
    # Total users
    c.execute('SELECT COUNT(*) as total_users FROM users')
    total_users = c.fetchone()['total_users']
    
    # Available slots
    c.execute('SELECT COUNT(*) as available FROM slots WHERE status = "available"')
    available_slots = c.fetchone()['available']
    
    conn.close()
    
    return jsonify({
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'active_parkings': active_parkings,
        'total_users': total_users,
        'available_slots': available_slots
    })

@app.route('/api/export')
def api_export():
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''SELECT pl.id, u.name, pl.vehicle_no, s.slot_number, 
                 pl.entry_time, pl.exit_time, pl.duration_minutes, pl.fee, pl.status
                 FROM parking_logs pl
                 LEFT JOIN users u ON pl.user_id = u.id
                 LEFT JOIN slots s ON pl.slot_id = s.id
                 ORDER BY pl.entry_time DESC''')
    logs = c.fetchall()
    
    conn.close()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Vehicle No', 'Slot', 'Entry Time', 'Exit Time', 'Duration (min)', 'Fee', 'Status'])
    
    for log in logs:
        writer.writerow([
            log['id'],
            log['name'] or 'N/A',
            log['vehicle_no'],
            log['slot_number'] or 'N/A',
            log['entry_time'] or 'N/A',
            log['exit_time'] or 'N/A',
            log['duration_minutes'] or 'N/A',
            log['fee'] or '0',
            log['status']
        ])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'parking_logs_{datetime.now().strftime("%Y%m%d")}.csv'
    )

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)

