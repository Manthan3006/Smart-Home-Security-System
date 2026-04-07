# 🎓 Premium Attendance System

A modern, corporate-grade attendance management system with **Glassmorphism UI**, **Real-time Face Recognition**, and **Advanced Analytics Dashboard**.

## ✨ Features

### 🎨 **Glassmorphism UI Design**
- Semi-transparent panels with frosted glass effects
- Soft shadows and rounded corners
- Modern gradient accents
- Responsive layout with smooth animations

### 📊 **Admin Analytics Dashboard**
- Real-time attendance statistics
- Interactive charts and visualizations
- Daily, weekly, and monthly trends
- Employee-wise attendance analysis

### 👥 **Employee Statistics Module**
- Individual employee performance tracking
- Attendance percentage calculations
- Present vs Late analysis
- Monthly attendance patterns

### 📷 **Advanced Face Recognition**
- Real-time camera processing
- Optimized performance (3x faster)
- Automatic attendance marking
- Time-based status (Present/Late)

### 🔐 **Secure Access Control**
- Role-based authentication
- Admin dashboard protection
- Encrypted password storage
- Session management

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Photos
Add employee photos to the `Pics/` folder:
```
Pics/
├── john_doe.jpg
├── jane_smith.png
├── mike_wilson.jpeg
└── sarah_jones.bmp
```

### 3. Run the System
```bash
python run_attendance_system.py
```

## 🎮 Usage Guide

### **Employee Mode**
1. Click "👤 Employee Mode"
2. Press "📷 Start Camera"
3. Face recognition runs automatically
4. Attendance marked when recognized

### **Admin Dashboard**
1. Click "🔐 Admin Dashboard"
2. Enter password (default: `admin123`)
3. View analytics and employee stats
4. Export reports and charts

## 📊 Dashboard Features

### **Analytics Overview**
- Today's attendance summary
- Present vs Late distribution
- Weekly attendance trends
- Top performing employees

### **Employee Statistics**
- Individual performance metrics
- Attendance percentage tracking
- Monthly attendance charts
- Historical data analysis

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Attendance Settings
REPORTING_TIME = time(10, 0)  # 10:00 AM cutoff

# Performance Settings  
FRAME_SKIP = 3  # Process every 3rd frame
RESIZE_FACTOR = 0.5  # 50% resolution for speed

# UI Theme
GLASSMORPHISM_COLORS = {
    'primary_bg': '#0D1117',
    'accent_blue': '#58A6FF',
    # ... more colors
}
```

## 📁 File Structure

```
attendance-system/
├── run_attendance_system.py    # Main launcher
├── attendance_ui.py           # UI and core logic
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── Pics/                      # Employee photos
├── attendance_records/        # CSV attendance files
└── admin_config.json         # Admin settings
```

## 🔧 Technical Details

### **Performance Optimizations**
- Frame skipping for real-time processing
- Resolution scaling for faster recognition
- HOG model for speed vs accuracy balance
- Multi-threading for UI responsiveness

### **Data Management**
- CSV-based attendance logging
- Pandas for data analysis
- Matplotlib/Plotly for visualizations
- JSON configuration storage

### **Security Features**
- SHA-256 password hashing
- Session-based authentication
- Role-based access control
- Secure admin configuration

## 📈 Analytics Capabilities

### **Dashboard Charts**
- **Pie Chart**: Today's Present vs Late
- **Line Chart**: Weekly attendance trends  
- **Bar Chart**: Employee attendance ranking
- **Area Chart**: Daily attendance patterns

### **Employee Reports**
- Individual attendance percentage
- Present vs Late breakdown
- Monthly attendance calendar
- Performance trend analysis

## 🎨 Glassmorphism Implementation

The UI uses advanced glassmorphism principles:

```python
class GlassmorphismFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        kwargs.setdefault('fg_color', ('gray90', 'gray13'))
        kwargs.setdefault('corner_radius', 20)
        kwargs.setdefault('border_width', 1)
        kwargs.setdefault('border_color', ('gray70', 'gray30'))
        super().__init__(parent, **kwargs)
```

## 🔐 Default Credentials

- **Admin Password**: `admin123`
- **Change in**: Admin Dashboard → Settings

## 📊 Export Features

- Export charts as PNG/PDF
- Generate attendance reports
- Backup attendance data
- Print-ready analytics

## 🛠️ Troubleshooting

### **Camera Issues**
```bash
# Check camera permissions
# Restart application
# Try different camera index
```

### **Face Recognition Problems**
```bash
# Ensure good lighting
# Use clear, front-facing photos
# Check Pics/ folder permissions
```

### **Performance Issues**
```bash
# Increase FRAME_SKIP in config.py
# Decrease RESIZE_FACTOR
# Close other camera applications
```

## 🚀 Advanced Features

### **Bonus Features Implemented**
- ✅ Animated UI transitions
- ✅ Hover effects on buttons
- ✅ Chart export functionality
- ✅ Dark mode optimized
- ✅ Sound notifications
- ✅ Real-time performance metrics

## 📞 Support

For issues or customization:
1. Check configuration in `config.py`
2. Review logs in console output
3. Ensure all dependencies installed
4. Verify camera permissions

---

**🎓 Premium Attendance System** - Modern corporate attendance management with style and performance.