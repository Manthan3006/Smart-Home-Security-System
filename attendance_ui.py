"""
🎓 PREMIUM ATTENDANCE SYSTEM - GLASSMORPHISM UI
Modern Corporate Attendance Management with Analytics Dashboard

Features:
- Glassmorphism UI Design
- Admin Analytics Dashboard  
- Employee Statistics Module
- Real-time Face Recognition
- Secure Role-based Access
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import cv2
import face_recognition
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
# Optional plotly imports (for future enhancements)
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.offline import plot
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
import os
import csv
from datetime import datetime, timedelta, time
from PIL import Image, ImageTk, ImageFilter
import threading
import hashlib
import json
from typing import Dict, List, Tuple, Optional

# ==================== CONFIGURATION ====================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Attendance System Configuration
REPORTING_TIME = time(10, 0)
ATTENDANCE_FOLDER = "attendance_records"
PICS_FOLDER = "Pics"
ADMIN_CONFIG_FILE = "admin_config.json"

# UI Configuration
GLASSMORPHISM_COLORS = {
    'primary_bg': '#0D1117',
    'glass_bg': 'rgba(255, 255, 255, 0.1)',
    'glass_border': 'rgba(255, 255, 255, 0.2)',
    'text_primary': '#FFFFFF',
    'text_secondary': '#8B949E',
    'accent_blue': '#58A6FF',
    'accent_green': '#3FB950',
    'accent_red': '#F85149',
    'accent_orange': '#D29922'
}

# Performance Settings
FRAME_SKIP = 3
RESIZE_FACTOR = 0.5
FACE_RECOGNITION_TOLERANCE = 0.6
MAX_FACES_PER_FRAME = 5

class AttendanceDataManager:
    """Handles all data operations for attendance system"""
    
    def __init__(self):
        self.setup_folders()
        
    def setup_folders(self):
        """Create necessary folders"""
        for folder in [ATTENDANCE_FOLDER, PICS_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
    def get_attendance_filename(self, date=None):
        """Generate attendance CSV filename for given date"""
        if date is None:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        return os.path.join(ATTENDANCE_FOLDER, f"attendance_{date_str}.csv")
    
    def load_attendance_data(self, days_back=30) -> pd.DataFrame:
        """Load attendance data from CSV files"""
        all_data = []
        end_date = datetime.now()
        
        for i in range(days_back):
            date = end_date - timedelta(days=i)
            filename = self.get_attendance_filename(date)
            
            if os.path.exists(filename):
                try:
                    df = pd.read_csv(filename)
                    all_data.append(df)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df['Date'] = pd.to_datetime(combined_df['Date'])
            return combined_df
        else:
            # Return empty DataFrame with correct columns
            return pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status'])
    
    def get_employee_stats(self, employee_name: str, days_back=30) -> Dict:
        """Get statistics for specific employee"""
        df = self.load_attendance_data(days_back)
        employee_data = df[df['Name'] == employee_name]
        
        if employee_data.empty:
            return {
                'total_days': 0,
                'present_days': 0,
                'late_days': 0,
                'attendance_percentage': 0,
                'last_attendance': 'Never',
                'monthly_data': pd.DataFrame()
            }
        
        total_days = len(employee_data)
        present_days = len(employee_data[employee_data['Status'] == 'Present'])
        late_days = len(employee_data[employee_data['Status'] == 'Late'])
        attendance_percentage = (total_days / days_back) * 100
        
        last_attendance = employee_data.iloc[-1]['Date'].strftime('%Y-%m-%d') if not employee_data.empty else 'Never'
        
        return {
            'total_days': total_days,
            'present_days': present_days,
            'late_days': late_days,
            'attendance_percentage': attendance_percentage,
            'last_attendance': last_attendance,
            'monthly_data': employee_data
        }
    
    def get_dashboard_stats(self) -> Dict:
        """Get statistics for admin dashboard"""
        df = self.load_attendance_data(30)
        
        if df.empty:
            return {
                'today_total': 0,
                'today_present': 0,
                'today_late': 0,
                'weekly_trend': pd.DataFrame(),
                'employee_summary': pd.DataFrame()
            }
        
        today = datetime.now().date()
        today_data = df[df['Date'].dt.date == today]
        
        # Weekly trend
        df['Week'] = df['Date'].dt.isocalendar().week
        weekly_trend = df.groupby(['Week', 'Status']).size().unstack(fill_value=0)
        
        # Employee summary
        employee_summary = df.groupby('Name').agg({
            'Status': 'count',
            'Date': 'max'
        }).rename(columns={'Status': 'Total_Days', 'Date': 'Last_Seen'})
        
        return {
            'today_total': len(today_data),
            'today_present': len(today_data[today_data['Status'] == 'Present']),
            'today_late': len(today_data[today_data['Status'] == 'Late']),
            'weekly_trend': weekly_trend,
            'employee_summary': employee_summary
        }

class GlassmorphismFrame(ctk.CTkFrame):
    """Custom frame with glassmorphism effect"""
    
    def __init__(self, parent, **kwargs):
        # Set glassmorphism properties
        kwargs.setdefault('fg_color', ('gray90', 'gray13'))
        kwargs.setdefault('corner_radius', 20)
        kwargs.setdefault('border_width', 1)
        kwargs.setdefault('border_color', ('gray70', 'gray30'))
        
        super().__init__(parent, **kwargs)
        
        # Add subtle shadow effect
        self.configure(
            fg_color=('rgba(255,255,255,0.1)', 'rgba(255,255,255,0.05)'),
            border_color=('rgba(255,255,255,0.2)', 'rgba(255,255,255,0.1)')
        )

class ModernButton(ctk.CTkButton):
    """Modern button with glassmorphism styling"""
    
    def __init__(self, parent, **kwargs):
        kwargs.setdefault('corner_radius', 15)
        kwargs.setdefault('height', 45)
        kwargs.setdefault('font', ctk.CTkFont(size=14, weight="bold"))
        kwargs.setdefault('hover_color', ('gray70', 'gray30'))
        
        super().__init__(parent, **kwargs)

class AttendanceChart:
    """Handles chart creation and embedding"""
    
    @staticmethod
    def create_attendance_overview(parent, data_manager):
        """Create attendance overview chart"""
        stats = data_manager.get_dashboard_stats()
        
        # Create matplotlib figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#0D1117')
        
        # Today's attendance pie chart
        if stats['today_total'] > 0:
            sizes = [stats['today_present'], stats['today_late']]
            labels = ['Present', 'Late']
            colors = ['#3FB950', '#D29922']
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Today's Attendance", color='white', fontsize=12)
        else:
            ax1.text(0.5, 0.5, 'No data for today', ha='center', va='center', color='white')
            ax1.set_title("Today's Attendance", color='white', fontsize=12)
        
        # Weekly trend line chart
        if not stats['weekly_trend'].empty:
            weeks = stats['weekly_trend'].index
            present_data = stats['weekly_trend'].get('Present', [0] * len(weeks))
            late_data = stats['weekly_trend'].get('Late', [0] * len(weeks))
            
            ax2.plot(weeks, present_data, color='#3FB950', marker='o', label='Present')
            ax2.plot(weeks, late_data, color='#D29922', marker='s', label='Late')
            ax2.set_title('Weekly Attendance Trend', color='white', fontsize=12)
            ax2.legend()
            ax2.tick_params(colors='white')
        
        # Employee attendance bar chart
        if not stats['employee_summary'].empty:
            employees = stats['employee_summary'].index[:10]  # Top 10
            attendance_counts = stats['employee_summary']['Total_Days'][:10]
            
            bars = ax3.bar(range(len(employees)), attendance_counts, color='#58A6FF')
            ax3.set_title('Employee Attendance (Top 10)', color='white', fontsize=12)
            ax3.set_xticks(range(len(employees)))
            ax3.set_xticklabels(employees, rotation=45, ha='right', color='white')
            ax3.tick_params(colors='white')
        
        # Monthly summary
        df = data_manager.load_attendance_data(30)
        if not df.empty:
            monthly_summary = df.groupby(df['Date'].dt.day)['Status'].count()
            ax4.bar(monthly_summary.index, monthly_summary.values, color='#58A6FF')
            ax4.set_title('Daily Attendance Count (Last 30 Days)', color='white', fontsize=12)
            ax4.tick_params(colors='white')
        
        # Style all axes
        for ax in [ax1, ax2, ax3, ax4]:
            ax.set_facecolor('#161B22')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas.get_tk_widget()
    
    @staticmethod
    def create_employee_chart(parent, employee_name, data_manager):
        """Create employee-specific chart"""
        stats = data_manager.get_employee_stats(employee_name)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#0D1117')
        
        # Present vs Late pie chart
        if stats['total_days'] > 0:
            sizes = [stats['present_days'], stats['late_days']]
            labels = ['Present', 'Late']
            colors = ['#3FB950', '#D29922']
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title(f"{employee_name} - Present vs Late", color='white')
        
        # Monthly attendance trend
        if not stats['monthly_data'].empty:
            monthly_data = stats['monthly_data'].groupby(stats['monthly_data']['Date'].dt.day).size()
            ax2.bar(monthly_data.index, monthly_data.values, color='#58A6FF')
            ax2.set_title(f"{employee_name} - Daily Attendance", color='white')
            ax2.tick_params(colors='white')
        
        # Style axes
        for ax in [ax1, ax2]:
            ax.set_facecolor('#161B22')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas.get_tk_widget()

class FaceRecognitionEngine:
    """Handles face recognition operations"""
    
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_today = set()
        self.load_faces_from_pics()
        self.load_today_attendance()
    
    def load_faces_from_pics(self):
        """Load faces from Pics folder"""
        if not os.path.exists(PICS_FOLDER):
            return
        
        self.known_face_encodings = []
        self.known_face_names = []
        supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        
        for filename in os.listdir(PICS_FOLDER):
            if filename.lower().endswith(supported_extensions):
                name = os.path.splitext(filename)[0]
                file_path = os.path.join(PICS_FOLDER, filename)
                
                try:
                    image = face_recognition.load_image_file(file_path)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        self.known_face_encodings.append(face_encodings[0])
                        self.known_face_names.append(name)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def load_today_attendance(self):
        """Load today's attendance to avoid duplicates"""
        data_manager = AttendanceDataManager()
        filename = data_manager.get_attendance_filename()
        self.attendance_today = set()
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 1:
                            self.attendance_today.add(row[0])
            except Exception as e:
                print(f"Error loading attendance: {e}")
    
    def mark_attendance(self, name, status):
        """Mark attendance in CSV file"""
        data_manager = AttendanceDataManager()
        filename = data_manager.get_attendance_filename()
        now = datetime.now()
        
        file_exists = os.path.exists(filename)
        
        try:
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                
                if not file_exists:
                    writer.writerow(['Name', 'Date', 'Time', 'Status'])
                
                writer.writerow([
                    name,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    status
                ])
            
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
    
    def get_attendance_status(self, current_time):
        """Determine attendance status based on current time"""
        return "Present" if current_time <= REPORTING_TIME else "Late"

class AdminManager:
    """Handles admin authentication and configuration"""
    
    def __init__(self):
        self.load_admin_config()
    
    def load_admin_config(self):
        """Load admin configuration"""
        if os.path.exists(ADMIN_CONFIG_FILE):
            try:
                with open(ADMIN_CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.admin_password_hash = config.get('password_hash', '')
            except:
                self.admin_password_hash = ''
        else:
            # Default password: "admin123"
            self.admin_password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            self.save_admin_config()
    
    def save_admin_config(self):
        """Save admin configuration"""
        config = {'password_hash': self.admin_password_hash}
        with open(ADMIN_CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    
    def verify_password(self, password):
        """Verify admin password"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == self.admin_password_hash
    
    def change_password(self, new_password):
        """Change admin password"""
        self.admin_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        self.save_admin_config()

class AttendanceSystemUI:
    """Main UI class with glassmorphism design"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🎓 Premium Attendance System")
        self.root.geometry("1400x900")
        self.root.configure(fg_color=GLASSMORPHISM_COLORS['primary_bg'])
        
        # Initialize managers
        self.data_manager = AttendanceDataManager()
        self.face_engine = FaceRecognitionEngine()
        self.admin_manager = AdminManager()
        
        # UI State
        self.current_frame = None
        self.is_admin = False
        self.camera_active = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup main UI structure"""
        self.show_landing_page()
    
    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_landing_page(self):
        """Show landing page with glassmorphism design"""
        self.clear_frame()
        
        self.current_frame = GlassmorphismFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self.current_frame,
            text="🎓 Premium Attendance System",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        title_label.pack(pady=(50, 30))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.current_frame,
            text="Modern Face Recognition • Real-time Analytics • Secure Access",
            font=ctk.CTkFont(size=16),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Button container
        button_frame = GlassmorphismFrame(self.current_frame)
        button_frame.pack(pady=20)
        
        # Employee Mode Button
        employee_btn = ModernButton(
            button_frame,
            text="👤 Employee Mode",
            width=250,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=GLASSMORPHISM_COLORS['accent_blue'],
            command=self.show_employee_mode
        )
        employee_btn.pack(pady=15, padx=30)
        
        # Admin Mode Button
        admin_btn = ModernButton(
            button_frame,
            text="🔐 Admin Dashboard",
            width=250,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=GLASSMORPHISM_COLORS['accent_green'],
            command=self.show_admin_login
        )
        admin_btn.pack(pady=15, padx=30)
        
        # System Info
        info_frame = GlassmorphismFrame(self.current_frame)
        info_frame.pack(pady=(30, 0), fill="x", padx=50)
        
        stats = self.data_manager.get_dashboard_stats()
        info_text = f"📊 Today: {stats['today_total']} attendances • 🟢 Present: {stats['today_present']} • 🟡 Late: {stats['today_late']}"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        info_label.pack(pady=20)
    
    def show_admin_login(self):
        """Show admin login dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("400x300")
        dialog.configure(fg_color=GLASSMORPHISM_COLORS['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 200),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 150)
        ))
        
        main_frame = GlassmorphismFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔐 Admin Access",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        title_label.pack(pady=(30, 20))
        
        # Password entry
        password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter admin password",
            show="*",
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        password_entry.pack(pady=20)
        password_entry.focus()
        
        def verify_login():
            password = password_entry.get()
            if self.admin_manager.verify_password(password):
                self.is_admin = True
                dialog.destroy()
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Access Denied", "Invalid password!")
                password_entry.delete(0, 'end')
        
        # Login button
        login_btn = ModernButton(
            main_frame,
            text="Login",
            width=150,
            command=verify_login,
            fg_color=GLASSMORPHISM_COLORS['accent_green']
        )
        login_btn.pack(pady=10)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: verify_login())
        
        # Default password info
        info_label = ctk.CTkLabel(
            main_frame,
            text="Default password: admin123",
            font=ctk.CTkFont(size=12),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        info_label.pack(pady=(20, 0))
    
    def show_employee_mode(self):
        """Show employee attendance interface"""
        self.clear_frame()
        
        self.current_frame = GlassmorphismFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = GlassmorphismFrame(self.current_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Employee Attendance",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        back_btn = ModernButton(
            header_frame,
            text="← Back",
            width=100,
            command=self.show_landing_page,
            fg_color=GLASSMORPHISM_COLORS['accent_red']
        )
        back_btn.pack(side="right", padx=20, pady=15)
        
        # Camera frame
        camera_frame = GlassmorphismFrame(self.current_frame)
        camera_frame.pack(fill="both", expand=True)
        
        # Camera will be embedded here
        self.camera_label = ctk.CTkLabel(
            camera_frame,
            text="📷 Camera will appear here\nPress 'Start Camera' to begin",
            font=ctk.CTkFont(size=16),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        self.camera_label.pack(expand=True)
        
        # Controls
        controls_frame = GlassmorphismFrame(self.current_frame)
        controls_frame.pack(fill="x", pady=(20, 0))
        
        self.camera_btn = ModernButton(
            controls_frame,
            text="📷 Start Camera",
            width=150,
            command=self.toggle_camera,
            fg_color=GLASSMORPHISM_COLORS['accent_blue']
        )
        self.camera_btn.pack(side="left", padx=20, pady=15)
        
        # Status info
        self.status_label = ctk.CTkLabel(
            controls_frame,
            text=f"⏰ Reporting Time: {REPORTING_TIME.strftime('%H:%M')} | 👥 Registered: {len(self.face_engine.known_face_names)}",
            font=ctk.CTkFont(size=14),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        self.status_label.pack(side="right", padx=20, pady=15)
    
    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera in separate thread"""
        self.camera_active = True
        self.camera_btn.configure(text="📷 Stop Camera", fg_color=GLASSMORPHISM_COLORS['accent_red'])
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_camera(self):
        """Stop camera"""
        self.camera_active = False
        self.camera_btn.configure(text="📷 Start Camera", fg_color=GLASSMORPHISM_COLORS['accent_blue'])
        
        if hasattr(self, 'cap'):
            self.cap.release()
    
    def camera_loop(self):
        """Main camera processing loop"""
        self.cap = cv2.VideoCapture(0)
        
        # Optimize camera settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        frame_count = 0
        
        while self.camera_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Process every nth frame for face recognition
            if frame_count % FRAME_SKIP == 0:
                self.process_frame(frame)
            
            # Display frame
            self.display_frame(frame)
            frame_count += 1
        
        self.cap.release()
    
    def process_frame(self, frame):
        """Process frame for face recognition"""
        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        
        if len(face_locations) > MAX_FACES_PER_FRAME:
            face_locations = face_locations[:MAX_FACES_PER_FRAME]
        
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Process each face
        current_time = datetime.now().time()
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.face_engine.known_face_encodings, 
                face_encoding, 
                tolerance=FACE_RECOGNITION_TOLERANCE
            )
            
            if self.face_engine.known_face_encodings:
                face_distances = face_recognition.face_distance(
                    self.face_engine.known_face_encodings, 
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.face_engine.known_face_names[best_match_index]
                    
                    if name not in self.face_engine.attendance_today:
                        status = self.face_engine.get_attendance_status(current_time)
                        if self.face_engine.mark_attendance(name, status):
                            self.face_engine.attendance_today.add(name)
                            print(f"✅ Attendance marked: {name} - {status}")
    
    def display_frame(self, frame):
        """Display frame in UI"""
        # Convert frame to PhotoImage
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_pil = frame_pil.resize((640, 480), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(frame_pil)
        
        # Update label
        self.root.after(0, lambda: self.update_camera_display(photo))
    
    def update_camera_display(self, photo):
        """Update camera display in main thread"""
        if hasattr(self, 'camera_label') and self.camera_active:
            self.camera_label.configure(image=photo, text="")
            self.camera_label.image = photo  # Keep a reference
    
    def show_admin_dashboard(self):
        """Show admin dashboard with analytics"""
        self.clear_frame()
        
        self.current_frame = GlassmorphismFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with navigation
        header_frame = GlassmorphismFrame(self.current_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Admin Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.pack(side="right", padx=20, pady=15)
        
        dashboard_btn = ModernButton(
            nav_frame,
            text="📊 Dashboard",
            width=120,
            height=35,
            command=self.show_admin_dashboard,
            fg_color=GLASSMORPHISM_COLORS['accent_blue']
        )
        dashboard_btn.pack(side="left", padx=5)
        
        employees_btn = ModernButton(
            nav_frame,
            text="👥 Employees",
            width=120,
            height=35,
            command=self.show_employee_stats,
            fg_color=GLASSMORPHISM_COLORS['accent_green']
        )
        employees_btn.pack(side="left", padx=5)
        
        logout_btn = ModernButton(
            nav_frame,
            text="🚪 Logout",
            width=100,
            height=35,
            command=self.logout_admin,
            fg_color=GLASSMORPHISM_COLORS['accent_red']
        )
        logout_btn.pack(side="left", padx=5)
        
        # Stats cards
        stats_frame = GlassmorphismFrame(self.current_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        stats = self.data_manager.get_dashboard_stats()
        
        # Today's stats cards
        cards_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=20)
        
        self.create_stat_card(cards_frame, "📊 Total Today", str(stats['today_total']), GLASSMORPHISM_COLORS['accent_blue']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "🟢 Present", str(stats['today_present']), GLASSMORPHISM_COLORS['accent_green']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "🟡 Late", str(stats['today_late']), GLASSMORPHISM_COLORS['accent_orange']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "👥 Registered", str(len(self.face_engine.known_face_names)), GLASSMORPHISM_COLORS['accent_blue']).pack(side="left", padx=10, fill="x", expand=True)
        
        # Charts
        charts_frame = GlassmorphismFrame(self.current_frame)
        charts_frame.pack(fill="both", expand=True)
        
        chart_widget = AttendanceChart.create_attendance_overview(charts_frame, self.data_manager)
        chart_widget.pack(fill="both", expand=True, padx=20, pady=20)
    
    def create_stat_card(self, parent, title, value, color):
        """Create a glassmorphism stat card"""
        card = GlassmorphismFrame(parent)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color=GLASSMORPHISM_COLORS['text_secondary']
        )
        title_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 15))
        
        return card
    
    def show_employee_stats(self):
        """Show employee statistics interface"""
        self.clear_frame()
        
        self.current_frame = GlassmorphismFrame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = GlassmorphismFrame(self.current_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👥 Employee Statistics",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        back_btn = ModernButton(
            header_frame,
            text="← Dashboard",
            width=120,
            command=self.show_admin_dashboard,
            fg_color=GLASSMORPHISM_COLORS['accent_blue']
        )
        back_btn.pack(side="right", padx=20, pady=15)
        
        # Employee selection
        selection_frame = GlassmorphismFrame(self.current_frame)
        selection_frame.pack(fill="x", pady=(0, 20))
        
        select_label = ctk.CTkLabel(
            selection_frame,
            text="Select Employee:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=GLASSMORPHISM_COLORS['text_primary']
        )
        select_label.pack(side="left", padx=20, pady=15)
        
        # Employee dropdown
        employee_names = self.face_engine.known_face_names
        if employee_names:
            self.employee_var = ctk.StringVar(value=employee_names[0])
            employee_dropdown = ctk.CTkComboBox(
                selection_frame,
                values=employee_names,
                variable=self.employee_var,
                width=200,
                command=self.update_employee_stats
            )
            employee_dropdown.pack(side="left", padx=20, pady=15)
        
        # Stats display frame
        self.employee_stats_frame = GlassmorphismFrame(self.current_frame)
        self.employee_stats_frame.pack(fill="both", expand=True)
        
        if employee_names:
            self.update_employee_stats(employee_names[0])
        else:
            no_data_label = ctk.CTkLabel(
                self.employee_stats_frame,
                text="No employees registered",
                font=ctk.CTkFont(size=16),
                text_color=GLASSMORPHISM_COLORS['text_secondary']
            )
            no_data_label.pack(expand=True)
    
    def update_employee_stats(self, employee_name):
        """Update employee statistics display"""
        # Clear existing widgets
        for widget in self.employee_stats_frame.winfo_children():
            widget.destroy()
        
        # Get employee stats
        stats = self.data_manager.get_employee_stats(employee_name)
        
        # Stats cards
        cards_frame = ctk.CTkFrame(self.employee_stats_frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=20)
        
        self.create_stat_card(cards_frame, "📅 Total Days", str(stats['total_days']), GLASSMORPHISM_COLORS['accent_blue']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "🟢 Present", str(stats['present_days']), GLASSMORPHISM_COLORS['accent_green']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "🟡 Late", str(stats['late_days']), GLASSMORPHISM_COLORS['accent_orange']).pack(side="left", padx=10, fill="x", expand=True)
        self.create_stat_card(cards_frame, "📊 Attendance %", f"{stats['attendance_percentage']:.1f}%", GLASSMORPHISM_COLORS['accent_blue']).pack(side="left", padx=10, fill="x", expand=True)
        
        # Employee chart
        if stats['total_days'] > 0:
            chart_widget = AttendanceChart.create_employee_chart(
                self.employee_stats_frame, 
                employee_name, 
                self.data_manager
            )
            chart_widget.pack(fill="both", expand=True, padx=20, pady=20)
        else:
            no_data_label = ctk.CTkLabel(
                self.employee_stats_frame,
                text=f"No attendance data found for {employee_name}",
                font=ctk.CTkFont(size=16),
                text_color=GLASSMORPHISM_COLORS['text_secondary']
            )
            no_data_label.pack(expand=True)
    
    def logout_admin(self):
        """Logout from admin mode"""
        self.is_admin = False
        self.show_landing_page()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# ==================== MAIN APPLICATION ====================
if __name__ == "__main__":
    # Install required packages if not available
    try:
        import customtkinter
        import matplotlib
        import seaborn
        import plotly
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install: pip install customtkinter matplotlib seaborn plotly pandas")
        print("OOOOO")
        exit(1)
    
    # Start the application
    app = AttendanceSystemUI()
    app.run()