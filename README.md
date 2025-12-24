# 🚗 QR Parking Management System

Automated parking management system with QR code-based entry/exit, real-time slot tracking, and automated billing.

## 🎯 Features

- ✅ **QR Code Generation** - Generate unique QR codes for each vehicle/user
- ✅ **Entry Management** - Scan QR code for parking entry and automatic slot assignment
- ✅ **Exit Management** - Scan QR code for exit with automatic fee calculation
- ✅ **Live Dashboard** - Real-time slot availability tracking
- ✅ **Admin Panel** - Comprehensive reports, revenue tracking, and user management
- ✅ **History & Export** - View parking logs and export data to CSV

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Backend**: Python Flask
- **Database**: SQLite
- **QR Code**: qrcode library for generation, jsQR for scanning

## 📦 Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "QR Parking"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to: `http://localhost:5000`

## 📱 Usage

### For Users:

1. **Register**: Go to `/register` and fill in your details to get a QR code
2. **Entry**: Go to `/entry` and scan your QR code when entering the parking
3. **Exit**: Go to `/exit` and scan your QR code when leaving (fee will be calculated automatically)

### For Admins:

1. **Dashboard**: Go to `/admin` to view:
   - Real-time slot availability
   - Revenue statistics
   - User list
   - Parking logs
   - Export data to CSV

## 💰 Billing Logic

- **First 30 minutes**: ₹20
- **Every additional 30 minutes**: ₹10

*(Configurable in the code)*

## 📂 Project Structure

```
QR Parking/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── parking.db            # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── index.html        # Home page
│   ├── register.html     # User registration
│   ├── entry.html        # Entry scanner
│   ├── exit.html         # Exit scanner
│   └── admin.html        # Admin dashboard
└── static/               # Static files (QR codes, etc.)
    └── qr_codes/         # Generated QR code images
```

## 🗃️ Database Schema

### Users Table
- `id` - Primary key
- `name` - User's full name
- `vehicle_no` - Vehicle number (unique)
- `qr_code` - Unique QR code identifier
- `phone` - Phone number (optional)
- `email` - Email address (optional)
- `created_at` - Registration timestamp

### Slots Table
- `id` - Primary key
- `slot_number` - Slot identifier (e.g., SLOT-001)
- `status` - Available/Occupied
- `vehicle_no` - Currently parked vehicle
- `entry_time` - Entry timestamp
- `qr_code` - QR code of parked vehicle

### Parking Logs Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `vehicle_no` - Vehicle number
- `slot_id` - Foreign key to slots
- `qr_code` - QR code used
- `entry_time` - Entry timestamp
- `exit_time` - Exit timestamp
- `duration_minutes` - Parking duration
- `fee` - Calculated parking fee
- `status` - Active/Completed

## 🔧 Configuration

- **Port**: Default is 5000 (change in `app.py`)
- **Slots**: Default is 50 slots (change in `init_db()` function)
- **Fee Structure**: Modify `calculate_fee()` function in `app.py`

## 📝 API Endpoints

- `GET /` - Home page
- `GET /register` - Registration page
- `GET /entry` - Entry scanner page
- `GET /exit` - Exit scanner page
- `GET /admin` - Admin dashboard
- `POST /api/register` - Register new user
- `POST /api/entry` - Process entry
- `POST /api/exit` - Process exit
- `GET /api/slots` - Get all slots
- `GET /api/users` - Get all users
- `GET /api/logs` - Get parking logs
- `GET /api/stats` - Get statistics
- `GET /api/export` - Export logs to CSV

## 🎨 Features in Detail

### QR Code Scanning
- Uses device camera for real-time QR scanning
- Fallback to manual QR code entry
- Works on mobile and desktop browsers

### Real-time Updates
- Admin dashboard auto-refreshes every 30 seconds
- Live slot availability display
- Real-time revenue tracking

### Data Export
- Export parking logs to CSV format
- Includes all transaction details
- Timestamped filename

## 🔒 Security Notes

- This is a basic implementation for demonstration
- For production use, consider:
  - Authentication/Authorization
  - Input validation and sanitization
  - HTTPS encryption
  - Rate limiting
  - SQL injection prevention (already using parameterized queries)

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project!

---

**Made with ❤️ for automated parking management**

