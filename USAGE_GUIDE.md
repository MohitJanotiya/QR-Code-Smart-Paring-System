# 📖 QR Parking System - Step-by-Step Usage Guide

## 🚀 Step 1: Start the Application

1. **Open Terminal** and navigate to the project directory:
   ```bash
   cd "/Users/mohit2002/Desktop/vs code/learning/pratice1.py/final/QR Parking"
   ```

2. **Run the application**:
   ```bash
   python3 app.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5001
   ```

---

## 👤 Step 2: Register a New User (First Time Only)

### For Vehicle Owners:

1. **Click on "User Registration"** from the home page or go to:
   ```
   http://localhost:5001/register
   ```

2. **Fill in the registration form**:
   - **Full Name*** (Required): Enter your name
   - **Vehicle Number*** (Required): Enter your vehicle number (e.g., MH12AB1234)
   - **Phone Number** (Optional): Your contact number
   - **Email** (Optional): Your email address

3. **Click "Generate QR Code"**

4. **Save your QR Code**:
   - The QR code image will appear on screen
   - **Print it** or **save it on your phone** for future use
   - The QR code data is unique to your vehicle

5. **Note**: You only need to register once. Keep your QR code safe!

---

## 🚗 Step 3: Parking Entry

### When Entering the Parking:

1. **Go to Entry Page**:
   - Click "Entry" from home page or visit:
   ```
   http://localhost:5001/entry
   ```

2. **Scan Your QR Code**:
   
   **Option A: Camera Scan (Recommended)**
   - Click **"Start Camera"** button
   - Allow camera access when prompted
   - Point your camera at the QR code
   - The system will automatically detect and process it

   **Option B: Manual Entry**
   - If camera doesn't work, enter the QR code data manually
   - Type the QR code data in the text field
   - Click **"Submit"**

3. **Confirmation**:
   - You'll see a success message with:
     - **Slot Number** assigned (e.g., SLOT-001)
     - **Entry Time** recorded
   - The slot is now marked as "Occupied"

4. **Park your vehicle** in the assigned slot!

---

## 🚪 Step 4: Parking Exit

### When Leaving the Parking:

1. **Go to Exit Page**:
   - Click "Exit" from home page or visit:
   ```
   http://localhost:5001/exit
   ```

2. **Scan Your QR Code Again**:
   
   **Option A: Camera Scan**
   - Click **"Start Camera"** button
   - Point camera at your QR code
   - System will automatically detect it

   **Option B: Manual Entry**
   - Enter QR code data manually if needed
   - Click **"Submit"**

3. **View Your Bill**:
   - The system will display:
     - **Slot Number** that was occupied
     - **Entry Time** (when you entered)
     - **Exit Time** (current time)
     - **Duration** (total parking time in minutes)
     - **Total Fee** (automatically calculated)

4. **Payment**:
   - Pay the displayed amount
   - The slot is automatically freed for next user

### 💰 Fee Calculation:
- **First 30 minutes**: ₹20
- **Every additional 30 minutes**: ₹10
- Example: 1 hour 15 minutes = ₹20 + ₹20 = ₹40

---

## 👨‍💼 Step 5: Admin Dashboard (For Administrators)

### Accessing Admin Panel:

1. **Go to Admin Dashboard**:
   - Click "Admin Panel" from home page or visit:
   ```
   http://localhost:5001/admin
   ```

### Dashboard Features:

#### 📊 Statistics Overview:
- **Total Revenue**: All-time earnings
- **Today's Revenue**: Earnings for current day
- **Active Parkings**: Currently parked vehicles
- **Available Slots**: Free slots right now

#### 🅿️ Slots Management Tab:
- View all parking slots in real-time
- **Green slots** = Available
- **Red slots** = Occupied
- Click **"Refresh"** to update status
- Auto-refreshes every 30 seconds

#### 👥 Users Tab:
- View all registered users
- See user details:
  - Name, Vehicle Number
  - Phone, Email
  - Registration date
- Click **"Refresh"** to see latest users

#### 📋 Parking Logs Tab:
- View all parking transactions
- See complete history:
  - Entry/Exit times
  - Duration and fees
  - Slot assignments
  - Status (Active/Completed)

#### 📥 Export Data:
- Click **"Export CSV"** button
- Download parking logs as CSV file
- Use for accounting, reports, or analysis

---

## 🔄 Complete Workflow Example

### Scenario: A customer parks for 2 hours

1. **Customer arrives**:
   - Goes to `/register` (if first time)
   - Gets QR code

2. **Entry**:
   - Goes to `/entry`
   - Scans QR code
   - Gets assigned SLOT-015
   - Parks vehicle

3. **Customer returns after 2 hours**:
   - Goes to `/exit`
   - Scans QR code
   - System calculates: 2 hours = ₹20 + (3 × ₹10) = ₹50
   - Pays ₹50
   - Slot SLOT-015 is freed

4. **Admin checks**:
   - Views `/admin` dashboard
   - Sees SLOT-015 is now available
   - Revenue increased by ₹50
   - Transaction logged in history

---

## 💡 Tips & Best Practices

### For Users:
- ✅ Keep your QR code safe (print it or save on phone)
- ✅ Scan QR code clearly for faster processing
- ✅ Use camera scan for convenience
- ✅ Check your bill before paying

### For Admins:
- ✅ Monitor dashboard regularly
- ✅ Export logs daily/weekly for records
- ✅ Check slot availability before peak hours
- ✅ Review revenue reports regularly

---

## 🆘 Troubleshooting

### QR Code Not Scanning?
- Ensure good lighting
- Hold QR code steady
- Try manual entry option
- Check if QR code is damaged

### Camera Not Working?
- Allow camera permissions in browser
- Use manual entry as alternative
- Try different browser (Chrome recommended)

### Slot Not Available?
- Check admin dashboard for availability
- Wait for a slot to free up
- Contact admin if all slots occupied

### Can't Access Server?
- Make sure `python3 app.py` is running
- Check if port 5001 is available
- Try refreshing the page

---

## 📱 Mobile Usage

The system works on mobile browsers too!

1. **On your phone**, open browser
2. Go to: `http://[your-computer-ip]:5001`
   - Find your computer's IP address
   - Example: `http://192.168.1.100:5001`
3. Use camera to scan QR codes easily
4. Perfect for on-the-go entry/exit

---

## 🔐 Security Notes

- This is a demo system
- For production, add authentication
- Keep database backups regularly
- Monitor for unauthorized access

---

**Happy Parking! 🚗✨**

