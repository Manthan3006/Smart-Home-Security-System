#!/usr/bin/env python3
"""
🎓 PREMIUM ATTENDANCE SYSTEM - WEB APPLICATION
Flask Backend with Face Recognition & Analytics
"""

from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import cv2
import face_recognition
import numpy as np
import pandas as pd
import os
import csv
import json
import hashlib
from datetime import datetime, time, timedelta
import threading
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Attendance System Configuration
REPORTING_TIME = time(10, 0)  # 10:00 AM
ATTENDANCE_FOLDER = "attendance_records"
PICS_FOLDER = "Pics"
ADMIN_CONFIG_FILE = "admin_config.json"

# Performance Settings
FRAME_SKIP = 3
RESIZE_FACTOR = 0.5
FACE_RECOGNITION_TOLERANCE = 0.6
MAX_FACES_PER_FRAME = 5

class AttendanceSystem:
    """Core attendance system logic"""
    
    def __init__(self):
        self.setup_folders()
        self.load_admin_config()
        self.load_faces()
        self.camera = None
        self.camera_active = False
        self.frame_count = 0
        self.current_frame = None
        self.recognition_results = []
        self.pending_attendance = None  # Store pending attendance for GPS processing
        
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
        
        # Always regenerate the default password hash to ensure it works
        self.admin_password_hash = generate_password_hash("admin123")
        self.save_admin_config()
        print("🔐 Admin password reset to: admin123")
    
    def save_admin_config(self):
        """Save admin configuration"""
        config = {'password_hash': self.admin_password_hash}
        with open(ADMIN_CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    
    def verify_admin_password(self, password):
        """Verify admin password"""
        return check_password_hash(self.admin_password_hash, password)
    
    def load_faces(self):
        """Load faces from Pics folder"""
        self.known_face_encodings = []
        self.known_face_names = []
        
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
    
    def get_attendance_filename(self, date=None):
        """Generate attendance CSV filename"""
        if date is None:
            date = datetime.now()
        date_str = date.strftime("%Y-%m-%d")
        return os.path.join(ATTENDANCE_FOLDER, f"attendance_{date_str}.csv")
    
    def load_today_attendance(self):
        """Load today's attendance"""
        filename = self.get_attendance_filename()
        attendance_today = set()
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', newline='') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 1:
                            attendance_today.add(row[0])
            except Exception as e:
                print(f"Error loading attendance: {e}")
        
        return attendance_today
    
    def mark_attendance(self, name, status, latitude=None, longitude=None, accuracy=None):
        """Mark attendance in CSV with GPS location"""
        filename = self.get_attendance_filename()
        now = datetime.now()
        
        file_exists = os.path.exists(filename)
        
        try:
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                
                if not file_exists:
                    writer.writerow(['Name', 'Date', 'Time', 'Status', 'Latitude', 'Longitude', 'Accuracy'])
                
                writer.writerow([
                    name,
                    now.strftime("%Y-%m-%d"),
                    now.strftime("%H:%M:%S"),
                    status,
                    latitude if latitude is not None else 'Not Available',
                    longitude if longitude is not None else 'Not Available',
                    accuracy if accuracy is not None else 'Not Available'
                ])
            
            location_info = f" at {latitude}, {longitude}" if latitude and longitude else " (location not available)"
            print(f"✅ Attendance marked: {name} - {status}{location_info}")
            return True
        except Exception as e:
            print(f"❌ Error marking attendance: {e}")
            return False
    
    def get_attendance_status(self, current_time):
        """Determine attendance status"""
        return "Present" if current_time <= REPORTING_TIME else "Late"
    
    def start_camera(self):
        """Start camera capture"""
        if self.camera_active:
            return
        
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.camera_active = True
        
        # Start camera thread
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_camera(self):
        """Stop camera capture safely"""
        print("🛑 Stopping camera...")
        self.camera_active = False
        
        # Wait a moment for camera thread to finish
        if hasattr(self, 'camera_thread') and self.camera_thread.is_alive():
            self.camera_thread.join(timeout=2.0)
        
        # Safely release camera
        if self.camera:
            try:
                self.camera.release()
                print("📷 Camera released successfully")
            except Exception as e:
                print(f"⚠️ Warning releasing camera: {e}")
            finally:
                self.camera = None
        
        # Clear current frame
        self.current_frame = None
        self.recognition_results = []
        print("✅ Camera stopped safely")
    
    def camera_loop(self):
        """Main camera processing loop with error handling"""
        attendance_today = self.load_today_attendance()
        
        try:
            while self.camera_active and self.camera:
                ret, frame = self.camera.read()
                if not ret:
                    print("⚠️ Failed to read frame, retrying...")
                    continue
                
                self.current_frame = frame.copy()
                
                # Process every nth frame for face recognition
                if self.frame_count % FRAME_SKIP == 0:
                    try:
                        self.process_frame(frame, attendance_today)
                    except Exception as e:
                        print(f"⚠️ Error processing frame: {e}")
                        # Continue loop even if processing fails
                
                self.frame_count += 1
                
        except Exception as e:
            print(f"❌ Camera loop error: {e}")
        finally:
            # Ensure camera is released
            if self.camera:
                try:
                    self.camera.release()
                except:
                    pass
            print("🔄 Camera loop ended")
    
    def process_frame(self, frame, attendance_today):
        """Process frame for face recognition with GPS support"""
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
        
        # Scale back face locations
        face_locations = [(int(top/RESIZE_FACTOR), int(right/RESIZE_FACTOR), 
                         int(bottom/RESIZE_FACTOR), int(left/RESIZE_FACTOR)) 
                        for (top, right, bottom, left) in face_locations]
        
        # Process faces
        current_time = datetime.now().time()
        results = []
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding, 
                tolerance=FACE_RECOGNITION_TOLERANCE
            )
            
            name = "Unknown"
            status = "Not Registered"
            
            if self.known_face_encodings:
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings, 
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    
                    if name in attendance_today:
                        status = "Already Marked"
                    else:
                        attendance_status = self.get_attendance_status(current_time)
                        # Mark attendance immediately without waiting for GPS
                        if self.mark_attendance(name, attendance_status):
                            attendance_today.add(name)
                            status = f"{attendance_status} ✓"
                        else:
                            status = "Error"
            
            results.append({
                'name': name,
                'status': status,
                'bbox': [left, top, right, bottom]
            })
        
        self.recognition_results = results
    
    def get_frame(self):
        """Get current frame with annotations - safe version"""
        if self.current_frame is None:
            # Return a black frame if no camera frame available
            black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(black_frame, "Camera Inactive", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return black_frame
        
        try:
            frame = self.current_frame.copy()
            
            # Draw recognition results
            for result in self.recognition_results:
                left, top, right, bottom = result['bbox']
                name = result['name']
                status = result['status']
                
                # Choose color based on status
                if name == "Unknown":
                    color = (0, 0, 255)  # Red
                elif "Already Marked" in status:
                    color = (255, 165, 0)  # Orange
                elif "Present" in status:
                    color = (0, 255, 0)  # Green
                elif "Late" in status:
                    color = (0, 255, 255)  # Yellow
                else:
                    color = (0, 0, 255)  # Red
                
                # Draw rectangle and labels
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 60), (right, bottom), color, cv2.FILLED)
                
                cv2.putText(frame, name, (left + 6, bottom - 35), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, status, (left + 6, bottom - 10), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
            
            return frame
            
        except Exception as e:
            print(f"⚠️ Error getting frame: {e}")
            # Return black frame on error
            black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(black_frame, "Camera Error", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return black_frame
    
    def load_attendance_data(self, days_back=30):
        """Load attendance data for analytics with GPS support"""
        all_data = []
        end_date = datetime.now()
        
        for i in range(days_back):
            date = end_date - timedelta(days=i)
            filename = self.get_attendance_filename(date)
            
            if os.path.exists(filename):
                try:
                    df = pd.read_csv(filename)
                    # Ensure GPS columns exist for backward compatibility
                    if 'Latitude' not in df.columns:
                        df['Latitude'] = 'Not Available'
                    if 'Longitude' not in df.columns:
                        df['Longitude'] = 'Not Available'
                    if 'Accuracy' not in df.columns:
                        df['Accuracy'] = 'Not Available'
                    all_data.append(df)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            combined_df['Date'] = pd.to_datetime(combined_df['Date'])
            return combined_df
        else:
            return pd.DataFrame(columns=['Name', 'Date', 'Time', 'Status', 'Latitude', 'Longitude', 'Accuracy'])
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        df = self.load_attendance_data(30)
        attendance_today = self.load_today_attendance()
        
        if df.empty:
            return {
                'today_total': len(attendance_today),
                'today_present': 0,
                'today_late': 0,
                'total_employees': len(self.known_face_names),
                'weekly_data': [],
                'daily_data': []
            }
        
        today = datetime.now().date()
        today_data = df[df['Date'].dt.date == today]
        
        # Weekly trend (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        weekly_data = df[df['Date'] >= week_ago]
        weekly_summary = weekly_data.groupby([weekly_data['Date'].dt.date, 'Status']).size().unstack(fill_value=0)
        
        # Daily data for chart
        daily_data = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).date()
            day_data = df[df['Date'].dt.date == date]
            daily_data.append({
                'date': date.strftime('%m-%d'),
                'present': len(day_data[day_data['Status'] == 'Present']),
                'late': len(day_data[day_data['Status'] == 'Late'])
            })
        
        return {
            'today_total': len(attendance_today),
            'today_present': len(today_data[today_data['Status'] == 'Present']),
            'today_late': len(today_data[today_data['Status'] == 'Late']),
            'total_employees': len(self.known_face_names),
            'weekly_data': weekly_summary.to_dict() if not weekly_summary.empty else {},
            'daily_data': list(reversed(daily_data))
        }
    
    def get_employee_stats(self, employee_name):
        """Get employee-specific statistics"""
        df = self.load_attendance_data(30)
        employee_data = df[df['Name'] == employee_name]
        
        if employee_data.empty:
            return {
                'total_days': 0,
                'present_days': 0,
                'late_days': 0,
                'attendance_percentage': 0,
                'last_attendance': 'Never',
                'monthly_data': []
            }
        
        total_days = len(employee_data)
        present_days = len(employee_data[employee_data['Status'] == 'Present'])
        late_days = len(employee_data[employee_data['Status'] == 'Late'])
        attendance_percentage = (total_days / 30) * 100
        
        last_attendance = employee_data.iloc[-1]['Date'].strftime('%Y-%m-%d') if not employee_data.empty else 'Never'
        
        # Monthly data
        monthly_data = []
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).date()
            day_data = employee_data[employee_data['Date'].dt.date == date]
            if not day_data.empty:
                status = day_data.iloc[0]['Status']
                monthly_data.append({
                    'date': date.strftime('%m-%d'),
                    'status': status
                })
        
        return {
            'total_days': total_days,
            'present_days': present_days,
            'late_days': late_days,
            'attendance_percentage': attendance_percentage,
            'last_attendance': last_attendance,
            'monthly_data': list(reversed(monthly_data))
        }

# Initialize attendance system
attendance_system = AttendanceSystem()

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/gps_test')
def gps_test():
    """GPS testing page"""
    return render_template('gps_test.html')

@app.route('/employee')
def employee():
    """Employee attendance page"""
    return render_template('employee.html')

@app.route('/admin/standalone_login')
def admin_standalone_login():
    """Standalone admin login page (no dependencies)"""
    return render_template('standalone_login.html')

@app.route('/admin/direct_login')
def admin_direct_login():
    """Direct admin login bypass for testing"""
    # Directly log in the admin
    session['admin_logged_in'] = True
    print("🔐 Direct admin login - bypassing password")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/simple_login')
def admin_simple_login():
    """Simple admin login page for troubleshooting"""
    return render_template('simple_login.html')

@app.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    stats = attendance_system.get_dashboard_stats()
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/admin/employee_stats')
def employee_stats():
    """Employee statistics page"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    employees = attendance_system.known_face_names
    return render_template('employee_stats.html', employees=employees)

# API Routes
@app.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    """Admin login API"""
    data = request.get_json()
    password = data.get('password', '')
    
    print(f"🔐 Login attempt with password: {password}")
    print(f"🔐 Stored hash: {attendance_system.admin_password_hash}")
    
    if attendance_system.verify_admin_password(password):
        session['admin_logged_in'] = True
        print("✅ Login successful")
        return jsonify({'success': True})
    else:
        print("❌ Login failed")
        return jsonify({'success': False, 'message': 'Invalid password'})

@app.route('/api/admin/reset_password', methods=['POST'])
def api_reset_admin_password():
    """Reset admin password to default (for testing)"""
    try:
        attendance_system.admin_password_hash = generate_password_hash("admin123")
        attendance_system.save_admin_config()
        print("🔐 Admin password reset to: admin123")
        return jsonify({'success': True, 'message': 'Password reset to admin123'})
    except Exception as e:
        print(f"❌ Error resetting password: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/admin/logout', methods=['POST'])
def api_admin_logout():
    """Admin logout API"""
    session.pop('admin_logged_in', None)
    return jsonify({'success': True})

@app.route('/api/stop_camera', methods=['POST'])
def api_stop_camera():
    """Stop camera API with error handling"""
    try:
        attendance_system.stop_camera()
        return jsonify({'success': True, 'message': 'Camera stopped successfully'})
    except Exception as e:
        print(f"❌ Error stopping camera: {e}")
        return jsonify({'success': False, 'message': f'Error stopping camera: {str(e)}'})

@app.route('/api/start_camera', methods=['POST'])
def api_start_camera():
    """Start camera API with error handling"""
    try:
        attendance_system.start_camera()
        return jsonify({'success': True, 'message': 'Camera started successfully'})
    except Exception as e:
        print(f"❌ Error starting camera: {e}")
        return jsonify({'success': False, 'message': f'Error starting camera: {str(e)}'})

@app.route('/api/log_gps_location', methods=['POST'])
def api_log_gps_location():
    """Log GPS location for the most recent attendance record"""
    try:
        data = request.get_json()
        
        # Extract GPS data
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        
        if not latitude or not longitude:
            return jsonify({'success': False, 'message': 'No GPS data provided'})
        
        # Update the most recent attendance record with GPS data
        filename = attendance_system.get_attendance_filename()
        
        if not os.path.exists(filename):
            return jsonify({'success': False, 'message': 'No attendance file found'})
        
        # Read the CSV file
        rows = []
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        if len(rows) < 2:  # Header + at least one record
            return jsonify({'success': False, 'message': 'No attendance records found'})
        
        # Update the last record if it doesn't have GPS data
        last_row = rows[-1]
        if len(last_row) >= 7:  # Already has GPS columns
            if last_row[4] == 'Not Available':  # Latitude column
                last_row[4] = str(latitude)
                last_row[5] = str(longitude)
                last_row[6] = str(accuracy)
        else:
            # Add GPS columns to existing record
            while len(last_row) < 7:
                last_row.append('Not Available')
            last_row[4] = str(latitude)
            last_row[5] = str(longitude)
            last_row[6] = str(accuracy)
        
        # Write back to file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        
        print(f"📍 GPS location added to attendance record: {latitude}, {longitude}")
        
        return jsonify({
            'success': True, 
            'message': 'GPS location logged successfully',
            'latitude': latitude,
            'longitude': longitude
        })
        
    except Exception as e:
        print(f"❌ Error logging GPS location: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/mark_attendance_with_gps', methods=['POST'])
def api_mark_attendance_with_gps():
    """Mark attendance with GPS location data"""
    try:
        data = request.get_json()
        
        # Extract GPS data
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        accuracy = data.get('accuracy')
        
        # Check if there's a pending attendance
        if not hasattr(attendance_system, 'pending_attendance') or not attendance_system.pending_attendance:
            return jsonify({'success': False, 'message': 'No pending attendance to process'})
        
        pending = attendance_system.pending_attendance
        
        # Check if the pending attendance is still valid (within 30 seconds)
        time_diff = (datetime.now() - pending['timestamp']).total_seconds()
        if time_diff > 30:
            attendance_system.pending_attendance = None
            return jsonify({'success': False, 'message': 'Attendance request expired'})
        
        # Mark attendance with GPS data
        success = attendance_system.mark_attendance(
            pending['name'], 
            pending['status'],
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy
        )
        
        if success:
            # Add to today's attendance
            attendance_today = attendance_system.load_today_attendance()
            attendance_today.add(pending['name'])
            
            # Clear pending attendance
            attendance_system.pending_attendance = None
            
            location_msg = f"Location: {latitude}, {longitude}" if latitude and longitude else "Location: Not available"
            
            return jsonify({
                'success': True, 
                'message': f'Attendance marked for {pending["name"]} - {pending["status"]}',
                'location_info': location_msg,
                'name': pending['name'],
                'status': pending['status']
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to mark attendance'})
            
    except Exception as e:
        print(f"❌ Error marking attendance with GPS: {e}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/recent_attendance')
def api_recent_attendance():
    """Get recent attendance records with GPS data"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get last 10 attendance records
        df = attendance_system.load_attendance_data(7)  # Last 7 days
        
        if df.empty:
            return jsonify({'records': []})
        
        # Sort by date and time, get most recent
        df_sorted = df.sort_values(['Date', 'Time'], ascending=False).head(10)
        
        records = []
        for _, row in df_sorted.iterrows():
            record = {
                'name': row['Name'],
                'date': row['Date'].strftime('%Y-%m-%d'),
                'time': row['Time'],
                'status': row['Status'],
                'latitude': row.get('Latitude', 'Not Available'),
                'longitude': row.get('Longitude', 'Not Available'),
                'accuracy': row.get('Accuracy', 'Not Available')
            }
            
            # Add Google Maps link if GPS data is available
            if (record['latitude'] != 'Not Available' and 
                record['longitude'] != 'Not Available' and
                record['latitude'] and record['longitude']):
                record['maps_link'] = f"https://maps.google.com/?q={record['latitude']},{record['longitude']}"
            else:
                record['maps_link'] = None
                
            records.append(record)
        
        return jsonify({'records': records})
        
    except Exception as e:
        print(f"❌ Error getting recent attendance: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard_stats')
def api_dashboard_stats():
    """Get dashboard statistics"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    stats = attendance_system.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/employee_stats/<employee_name>')
def api_employee_stats(employee_name):
    """Get employee statistics"""
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    stats = attendance_system.get_employee_stats(employee_name)
    return jsonify(stats)

@app.route('/video_feed')
def video_feed():
    """Video streaming route with error handling"""
    def generate():
        while True:
            try:
                frame = attendance_system.get_frame()
                if frame is not None:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    if ret:
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                    else:
                        # If encoding fails, wait and continue
                        import time
                        time.sleep(0.1)
                else:
                    # If no frame available, wait and continue
                    import time
                    time.sleep(0.1)
            except Exception as e:
                print(f"⚠️ Video feed error: {e}")
                # Send a black frame on error
                black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(black_frame, "Video Error", (200, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                ret, buffer = cv2.imencode('.jpg', black_frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                import time
                time.sleep(0.5)
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("🎓 Premium Attendance System - Web Application")
    print("=" * 50)
    print("🚀 Starting Flask server...")
    print("📱 Access at: http://127.0.0.1:8000")
    print("🔐 Default admin password: admin123")
    print("=" * 50)
    print("trigger pipeline")
    
    app.run(debug=True, host='127.0.0.1', port=8000, threaded=True)