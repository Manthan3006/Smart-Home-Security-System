#!/usr/bin/env python3
"""
🎓 HOME SECURITY SYSTEM - SIMPLIFIED VERSION
Modern Home Security Management with Glassmorphism UI
Handles import issues gracefully
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys

# Try to import required packages with fallbacks
try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    print("CustomTkinter not available, using standard tkinter")
    CTK_AVAILABLE = False

try:
    import cv2
    import face_recognition
    import numpy as np
    CV_AVAILABLE = True
except ImportError:
    print("OpenCV or face_recognition not available")
    CV_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    print("Pandas not available, using basic data handling")
    PANDAS_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("Matplotlib not available, charts will be disabled")
    MATPLOTLIB_AVAILABLE = False

import csv
from datetime import datetime, timedelta, time
import threading
import hashlib
import json
from typing import Dict, List, Tuple, Optional

# Configuration
if CTK_AVAILABLE:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

REPORTING_TIME = time(10, 0)
ATTENDANCE_FOLDER = "attendance_records"
PICS_FOLDER = "Pics"
ADMIN_CONFIG_FILE = "admin_config.json"

# Performance Settings
FRAME_SKIP = 3
RESIZE_FACTOR = 0.5
FACE_RECOGNITION_TOLERANCE = 0.6
MAX_FACES_PER_FRAME = 5

# UI Colors
COLORS = {
    'primary_bg': '#0D1117',
    'text_primary': '#FFFFFF',
    'text_secondary': '#8B949E',
    'accent_blue': '#58A6FF',
    'accent_green': '#3FB950',
    'accent_red': '#F85149',
    'accent_orange': '#D29922'
}

class SimpleHomeSecuritySystem:
    """Simplified home security system with graceful fallbacks"""
    
    def __init__(self):
        # Initialize based on available packages
        if CTK_AVAILABLE:
            self.root = ctk.CTk()
            self.root.configure(fg_color=COLORS['primary_bg'])
        else:
            self.root = tk.Tk()
            self.root.configure(bg='#2b2b2b')
        
        self.root.title("🎓 Home Security System")
        self.root.geometry("1200x800")
        
        self.setup_folders()
        self.load_admin_config()
        self.load_faces()
        self.is_admin = False
        self.camera_active = False
        
        self.setup_ui()
    
    def setup_folders(self):
        """Create necessary folders"""
        for folder in [ATTENDANCE_FOLDER, PICS_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    
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
    
    def load_faces(self):
        """Load faces from Pics folder"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.attendance_today = set()
        
        if not CV_AVAILABLE:
            print("Face recognition not available - running in demo mode")
            return
        
        if not os.path.exists(PICS_FOLDER):
            return
        
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
                        print(f"✅ Loaded: {name}")
                except Exception as e:
                    print(f"❌ Error loading {filename}: {e}")
        
        print(f"📋 Loaded {len(self.known_face_names)} faces")
        self.load_today_attendance()
    
    def load_today_attendance(self):
        """Load today's entries"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.csv")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 1:
                            self.attendance_today.add(row[0])
            except Exception as e:
                print(f"Error loading entries: {e}")
    
    def mark_attendance(self, name, status):
        """Mark attendance in CSV"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.csv")
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
            
            print(f"✅ Entry marked: {name} - {status}")
            return True
        except Exception as e:
            print(f"❌ Error marking entry: {e}")
            return False
    
    def setup_ui(self):
        """Setup main UI"""
        self.show_landing_page()
    
    def clear_frame(self):
        """Clear current frame"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_frame(self, **kwargs):
        """Create frame based on available packages"""
        if CTK_AVAILABLE:
            return ctk.CTkFrame(self.root, corner_radius=20, **kwargs)
        else:
            return tk.Frame(self.root, bg='#3b3b3b', relief='raised', bd=2, **kwargs)
    
    def create_label(self, parent, text, **kwargs):
        """Create label based on available packages"""
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return tk.Label(parent, text=text, bg='#3b3b3b', fg='white', **kwargs)
    
    def create_button(self, parent, text, command, **kwargs):
        """Create button based on available packages"""
        if CTK_AVAILABLE:
            return ctk.CTkButton(parent, text=text, command=command, corner_radius=15, height=45, **kwargs)
        else:
            return tk.Button(parent, text=text, command=command, bg='#4CAF50', fg='white', relief='flat', **kwargs)
    
    def show_landing_page(self):
        """Show landing page"""
        self.clear_frame()
        
        # Main frame
        main_frame = self.create_frame()
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = self.create_label(
            main_frame,
            "🎓 Home Security System",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(50, 30))
        
        # Subtitle
        subtitle = self.create_label(
            main_frame,
            "Modern Face Recognition • Real-time Analytics • Secure Access"
        )
        subtitle.pack(pady=(0, 50))
        
        # Buttons
        button_frame = self.create_frame()
        button_frame.pack(pady=20)
        
        employee_btn = self.create_button(
            button_frame,
            "👤 Security Mode",
            self.show_employee_mode,
            width=250
        )
        employee_btn.pack(pady=15, padx=30)
        
        admin_btn = self.create_button(
            button_frame,
            "🔐 Admin Dashboard",
            self.show_admin_login,
            width=250
        )
        admin_btn.pack(pady=15, padx=30)
        
        # System info
        info_text = f"👥 Registered: {len(self.known_face_names)} | 📊 Today: {len(self.attendance_today)} attendances"
        info = self.create_label(main_frame, info_text)
        info.pack(pady=(30, 0))
    
    def show_admin_login(self):
        """Show admin login"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Admin Login")
        dialog.geometry("400x300")
        dialog.configure(bg='#2b2b2b')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center dialog
        dialog.geometry("+{}+{}".format(
            int(self.root.winfo_x() + self.root.winfo_width()/2 - 200),
            int(self.root.winfo_y() + self.root.winfo_height()/2 - 150)
        ))
        
        # Title
        title = tk.Label(dialog, text="🔐 Admin Access", font=("Arial", 20, "bold"), 
                        bg='#2b2b2b', fg='white')
        title.pack(pady=(30, 20))
        
        # Password entry
        password_entry = tk.Entry(dialog, show="*", font=("Arial", 14), width=20)
        password_entry.pack(pady=20)
        password_entry.focus()
        
        def verify_login():
            password = password_entry.get()
            if self.verify_password(password):
                self.is_admin = True
                dialog.destroy()
                self.show_admin_dashboard()
            else:
                messagebox.showerror("Access Denied", "Invalid password!")
                password_entry.delete(0, 'end')
        
        # Login button
        login_btn = tk.Button(dialog, text="Login", command=verify_login,
                             bg='#4CAF50', fg='white', font=("Arial", 12), width=15)
        login_btn.pack(pady=10)
        
        # Bind Enter key
        password_entry.bind('<Return>', lambda e: verify_login())
        
        # Info
        info = tk.Label(dialog, text="Default password: admin123", 
                       bg='#2b2b2b', fg='gray')
        info.pack(pady=(20, 0))
    
    def show_employee_mode(self):
        """Show employee mode"""
        self.clear_frame()
        
        # Header
        header_frame = self.create_frame()
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = self.create_label(header_frame, "👤 Face Recognition Entry", 
                                 font=("Arial", 24, "bold"))
        title.pack(side="left", padx=20, pady=15)
        
        back_btn = self.create_button(header_frame, "← Back", self.show_landing_page)
        back_btn.pack(side="right", padx=20, pady=15)
        
        # Camera frame
        camera_frame = self.create_frame()
        camera_frame.pack(fill="both", expand=True)
        
        if CV_AVAILABLE:
            self.camera_label = self.create_label(
                camera_frame,
                "📷 Camera ready\nPress 'Start Camera' to begin"
            )
            self.camera_label.pack(expand=True)
            
            # Controls
            controls_frame = self.create_frame()
            controls_frame.pack(fill="x", pady=(20, 0))
            
            self.camera_btn = self.create_button(
                controls_frame,
                "📷 Start Camera",
                self.toggle_camera
            )
            self.camera_btn.pack(side="left", padx=20, pady=15)
        else:
            no_camera = self.create_label(
                camera_frame,
                "❌ Camera not available\nOpenCV and face_recognition packages required"
            )
            no_camera.pack(expand=True)
        
        # Status
        status_text = f"⏰ Reporting: {REPORTING_TIME.strftime('%H:%M')} | 👥 Registered: {len(self.known_face_names)}"
        status = self.create_label(camera_frame, status_text)
        status.pack(pady=20)
    
    def show_admin_dashboard(self):
        """Show admin dashboard"""
        self.clear_frame()
        
        # Header
        header_frame = self.create_frame()
        header_frame.pack(fill="x", pady=(0, 20))
        
        title = self.create_label(header_frame, "📊 Admin Dashboard", 
                                 font=("Arial", 24, "bold"))
        title.pack(side="left", padx=20, pady=15)
        
        logout_btn = self.create_button(header_frame, "🚪 Logout", self.logout_admin)
        logout_btn.pack(side="right", padx=20, pady=15)
        
        # Stats
        stats_frame = self.create_frame()
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Load attendance data
        today_count = len(self.attendance_today)
        total_employees = len(self.known_face_names)
        
        stats_text = f"""
📊 ATTENDANCE STATISTICS

📅 Today's Entries: {today_count}
👥 Total Registered: {total_employees}
⏰ Reporting Time: {REPORTING_TIME.strftime('%H:%M')}
📁 Data Folder: {ATTENDANCE_FOLDER}
        """
        
        stats_label = self.create_label(stats_frame, stats_text, font=("Arial", 14))
        stats_label.pack(pady=20)
        
        # Employee list
        if self.known_face_names:
            employees_frame = self.create_frame()
            employees_frame.pack(fill="both", expand=True)
            
            emp_title = self.create_label(employees_frame, "👥 Registered Employees", 
                                         font=("Arial", 18, "bold"))
            emp_title.pack(pady=(20, 10))
            
            # Create scrollable list
            if CTK_AVAILABLE:
                scrollable_frame = ctk.CTkScrollableFrame(employees_frame)
                scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
            else:
                scrollable_frame = tk.Frame(employees_frame, bg='#3b3b3b')
                scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            for i, name in enumerate(self.known_face_names, 1):
                status = "✅ Present" if name in self.attendance_today else "⏸️ Not marked"
                emp_text = f"{i}. {name} - {status}"
                emp_label = self.create_label(scrollable_frame, emp_text)
                emp_label.pack(anchor="w", pady=2, padx=10)
        
        # Charts section (if matplotlib available)
        if MATPLOTLIB_AVAILABLE:
            charts_btn = self.create_button(
                stats_frame,
                "📈 View Charts",
                self.show_charts
            )
            charts_btn.pack(pady=10)
    
    def show_charts(self):
        """Show basic charts"""
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showinfo("Charts", "Matplotlib not available for charts")
            return
        
        # Create chart window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("📈 Attendance Charts")
        chart_window.geometry("800x600")
        chart_window.configure(bg='#2b2b2b')
        
        # Simple attendance chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#2b2b2b')
        
        # Today's attendance
        present_count = len(self.attendance_today)
        not_present_count = len(self.known_face_names) - present_count
        
        if present_count > 0 or not_present_count > 0:
            ax1.pie([present_count, not_present_count], 
                   labels=['Present', 'Not Present'],
                   colors=['#3FB950', '#F85149'],
                   autopct='%1.1f%%')
            ax1.set_title("Today's Entries", color='white')
        
        # Employee count bar
        if self.known_face_names:
            names = self.known_face_names[:10]  # Top 10
            statuses = [1 if name in self.attendance_today else 0 for name in names]
            
            ax2.bar(range(len(names)), statuses, color='#58A6FF')
            ax2.set_title('Employee Status', color='white')
            ax2.set_xticks(range(len(names)))
            ax2.set_xticklabels(names, rotation=45, ha='right', color='white')
            ax2.tick_params(colors='white')
        
        # Style
        for ax in [ax1, ax2]:
            ax.set_facecolor('#3b3b3b')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        plt.tight_layout()
        
        # Embed chart
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def toggle_camera(self):
        """Toggle camera"""
        if not CV_AVAILABLE:
            messagebox.showerror("Error", "Camera not available")
            return
        
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start camera"""
        self.camera_active = True
        self.camera_btn.configure(text="📷 Stop Camera")
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_camera(self):
        """Stop camera"""
        self.camera_active = False
        self.camera_btn.configure(text="📷 Start Camera")
        
        if hasattr(self, 'cap'):
            self.cap.release()
    
    def camera_loop(self):
        """Camera processing loop"""
        self.cap = cv2.VideoCapture(0)
        
        # Optimize settings
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        frame_count = 0
        
        while self.camera_active:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Process every nth frame
            if frame_count % FRAME_SKIP == 0:
                self.process_frame(frame)
            
            frame_count += 1
        
        self.cap.release()
    
    def process_frame(self, frame):
        """Process frame for face recognition"""
        if not self.known_face_encodings:
            return
        
        # Resize for speed
        small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Find faces
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        
        if len(face_locations) > MAX_FACES_PER_FRAME:
            face_locations = face_locations[:MAX_FACES_PER_FRAME]
        
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Process faces
        current_time = datetime.now().time()
        
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=FACE_RECOGNITION_TOLERANCE
            )
            
            if self.known_face_encodings:
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    
                    if name not in self.attendance_today:
                        status = "Present" if current_time <= REPORTING_TIME else "Late"
                        if self.mark_attendance(name, status):
                            self.attendance_today.add(name)
    
    def logout_admin(self):
        """Logout admin"""
        self.is_admin = False
        self.show_landing_page()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🎓 Home Security System - Simplified Version")
    print("=" * 50)
    
    # Check available packages
    missing_packages = []
    
    if not CTK_AVAILABLE:
        missing_packages.append("customtkinter")
    
    if not CV_AVAILABLE:
        missing_packages.append("opencv-python face-recognition")
    
    if not PANDAS_AVAILABLE:
        missing_packages.append("pandas")
    
    if not MATPLOTLIB_AVAILABLE:
        missing_packages.append("matplotlib seaborn")
    
    if missing_packages:
        print("⚠️ Some packages are missing:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nThe system will run with reduced functionality.")
        print("To install missing packages:")
        print("pip install customtkinter opencv-python face-recognition pandas matplotlib seaborn")
        print()
    
    print("🚀 Starting system...")
    print("Default admin password: admin123")
    print("=" * 50)
    
    try:
        app = SimpleHomeSecuritySystem()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Please check that all required packages are installed.")

if __name__ == "__main__":
    main()