import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime, time
from tkinter import filedialog, messagebox, simpledialog
import tkinter as tk

# ==================== ATTENDANCE SYSTEM CONFIGURATION ====================
REPORTING_TIME = time(10, 0)  # 10:00 AM - Change this as needed
ATTENDANCE_FOLDER = "attendance_records"
PICS_FOLDER = "Pics"  # Default folder for face photos

# ==================== PERFORMANCE OPTIMIZATION SETTINGS ====================
FRAME_SKIP = 3  # Process every 3rd frame for face recognition
RESIZE_FACTOR = 0.5  # Resize frame to 50% for faster processing
FACE_RECOGNITION_TOLERANCE = 0.6  # Face matching tolerance
MAX_FACES_PER_FRAME = 5  # Limit number of faces to process per frame

def setup_folders():
    """Create necessary folders if they don't exist"""
    # Create attendance folder
    if not os.path.exists(ATTENDANCE_FOLDER):
        os.makedirs(ATTENDANCE_FOLDER)
        print(f"Created attendance folder: {ATTENDANCE_FOLDER}")
    
    # Create Pics folder
    if not os.path.exists(PICS_FOLDER):
        os.makedirs(PICS_FOLDER)
        print(f"Created photos folder: {PICS_FOLDER}")
        print(f"📸 Add photos to '{PICS_FOLDER}' folder (filename = person's name)")

def load_faces_from_pics_folder():
    """Automatically load all known faces from the Pics folder"""
    if not os.path.exists(PICS_FOLDER):
        print(f"❌ '{PICS_FOLDER}' folder not found. Creating it...")
        os.makedirs(PICS_FOLDER)
        print(f"📸 Please add photos to '{PICS_FOLDER}' folder and restart the system")
        return [], []
    
    known_face_encodings = []
    known_face_names = []
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    
    print(f"📂 Loading faces from: {PICS_FOLDER}")
    
    # Get all image files in the Pics folder
    image_files = [f for f in os.listdir(PICS_FOLDER) if f.lower().endswith(supported_extensions)]
    
    if not image_files:
        print(f"⚠️  No image files found in '{PICS_FOLDER}' folder")
        print(f"📸 Please add photos to '{PICS_FOLDER}' folder (filename = person's name)")
        return [], []
    
    for filename in image_files:
        # Extract name from filename (remove extension)
        name = os.path.splitext(filename)[0]
        file_path = os.path.join(PICS_FOLDER, filename)
        
        try:
            print(f"Processing: {filename} -> {name}")
            image = face_recognition.load_image_file(file_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                print(f"  ⚠️  No face found in {filename}")
                continue
            
            if len(face_encodings) > 1:
                print(f"  ⚠️  Multiple faces found in {filename}, using the first one")
            
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(name)
            print(f"  ✅ Successfully loaded {name}")
            
        except Exception as e:
            print(f"  ❌ Error loading {filename}: {str(e)}")
    
    print(f"\n📋 Loaded {len(known_face_encodings)} known faces from '{PICS_FOLDER}':")
    for name in known_face_names:
        print(f"  - {name}")
    
    return known_face_encodings, known_face_names

def get_attendance_filename():
    """Generate today's attendance CSV filename"""
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.csv")

def load_today_attendance():
    """Load today's attendance records to avoid duplicates"""
    filename = get_attendance_filename()
    attendance_today = set()
    
    if os.path.exists(filename):
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 1:
                        attendance_today.add(row[0])  # Add name to set
        except Exception as e:
            print(f"Error loading attendance: {e}")
    
    return attendance_today

def mark_attendance(name, status):
    """Mark attendance in CSV file"""
    filename = get_attendance_filename()
    now = datetime.now()
    
    # Check if file exists, if not create with header
    file_exists = os.path.exists(filename)
    
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            
            # Write header if new file
            if not file_exists:
                writer.writerow(['Name', 'Date', 'Time', 'Status'])
            
            # Write attendance record
            writer.writerow([
                name,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                status
            ])
        
        print(f"✅ Attendance marked: {name} - {status} at {now.strftime('%H:%M:%S')}")
        return True
        
    except Exception as e:
        print(f"❌ Error marking attendance: {e}")
        return False

def get_attendance_status(current_time):
    """Determine attendance status based on current time"""
    if current_time <= REPORTING_TIME:
        return "Present"
    else:
        return "Late"

def play_attendance_sound():
    """Play sound when attendance is marked (optional)"""
    try:
        # Simple beep sound (works on most systems)
        print("\a")  # ASCII bell character
    except:
        pass

# ==================== FACE LOADING FUNCTIONS ====================
def load_single_face():
    """Function to load a single known face image"""
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(
        title="Select a photo of the person to recognize",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    
    if not file_path:
        return None, None
    
    root.deiconify()
    name = tk.simpledialog.askstring("Person Name", "Enter the person's name:")
    root.destroy()
    
    if not name:
        return None, None
    
    try:
        known_image = face_recognition.load_image_file(file_path)
        face_encodings = face_recognition.face_encodings(known_image)
        
        if len(face_encodings) == 0:
            messagebox.showerror("Error", "No face found in the selected image!")
            return None, None
        
        return face_encodings[0], name
        
    except Exception as e:
        messagebox.showerror("Error", f"Error loading image: {str(e)}")
        return None, None

# ==================== MAIN ATTENDANCE SYSTEM ====================
def main():
    print("=== 🎓 ATTENDANCE SYSTEM ===")
    print(f"📅 Today: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"⏰ Reporting Time: {REPORTING_TIME.strftime('%H:%M')}")
    print(f"📁 Attendance Records: {ATTENDANCE_FOLDER}")
    print(f"📸 Photos Folder: {PICS_FOLDER}")
    
    # Setup folders
    setup_folders()
    
    # Load today's attendance to avoid duplicates
    attendance_today = load_today_attendance()
    print(f"📋 Already marked today: {len(attendance_today)} people")
    
    # Automatically load known faces from Pics folder
    print(f"\n🔄 Loading faces from '{PICS_FOLDER}' folder...")
    known_face_encodings, known_face_names = load_faces_from_pics_folder()
    
    if len(known_face_encodings) == 0:
        print(f"\n⚠️  No faces loaded from '{PICS_FOLDER}' folder!")
        print(f"📸 Please add photos to '{PICS_FOLDER}' folder and restart")
        print(f"💡 Photo naming: 'john.jpg' will be recognized as 'john'")
        print("Exiting... Please add photos to 'Pics' folder and restart.")
        return
    
    # Initialize camera with optimized settings
    print(f"\n🎥 Starting optimized attendance camera...")
    print("Performance optimizations enabled:")
    print(f"  📊 Frame processing: Every {FRAME_SKIP} frames")
    print(f"  🔍 Resolution scaling: {int(RESIZE_FACTOR*100)}%")
    print(f"  👥 Max faces per frame: {MAX_FACES_PER_FRAME}")
    print("Controls:")
    print("  'q' - Quit system")
    print("  's' - Add single person manually")
    print("  'r' - Reload faces from Pics folder")
    print("  'v' - View attendance report")
    print(f"  💡 To add new people: Add photos to '{PICS_FOLDER}' folder and press 'r'")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open camera")
        return
    
    # Optimize camera settings for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Lower resolution for speed
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)            # Set FPS
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)      # Reduce buffer to minimize lag
    
    # Performance tracking variables
    frame_count = 0
    process_this_frame = True
    face_locations = []
    face_encodings = []
    face_names = []
    
    print("🚀 Camera optimized and ready!")
    
    # Main attendance loop with performance optimizations
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # ==================== PERFORMANCE OPTIMIZATION ====================
        # Only process every nth frame for face recognition
        if frame_count % FRAME_SKIP == 0:
            process_this_frame = True
        else:
            process_this_frame = False
        
        frame_count += 1
        
        if process_this_frame:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find faces in the resized frame
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")  # Use HOG model (faster)
            
            # Limit number of faces to process
            if len(face_locations) > MAX_FACES_PER_FRAME:
                face_locations = face_locations[:MAX_FACES_PER_FRAME]
            
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            # Scale back face locations to original frame size
            face_locations = [(int(top/RESIZE_FACTOR), int(right/RESIZE_FACTOR), 
                             int(bottom/RESIZE_FACTOR), int(left/RESIZE_FACTOR)) 
                            for (top, right, bottom, left) in face_locations]
            
            # Process face recognition
            face_names = []
            current_time = datetime.now().time()
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=FACE_RECOGNITION_TOLERANCE)
                name = "Unknown"
                attendance_status = ""
                
                if known_face_encodings:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        
                        # ==================== ATTENDANCE LOGIC ====================
                        if name in attendance_today:
                            attendance_status = "Already Marked"
                        else:
                            status = get_attendance_status(current_time)
                            if mark_attendance(name, status):
                                attendance_today.add(name)
                                attendance_status = f"{status} ✓"
                                play_attendance_sound()
                            else:
                                attendance_status = "Error"
                    else:
                        attendance_status = "Not Registered"
                else:
                    attendance_status = "Not Registered"
                
                face_names.append((name, attendance_status))
        
        # ==================== DISPLAY LOGIC (ALWAYS RUNS) ====================
        # Draw results on every frame for smooth display
        for (top, right, bottom, left), (name, attendance_status) in zip(face_locations, face_names):
            # Choose color based on status
            if name == "Unknown":
                color = (0, 0, 255)  # Red
            elif "Already Marked" in attendance_status:
                color = (255, 165, 0)  # Orange
            elif "Present" in attendance_status:
                color = (0, 255, 0)  # Green
            elif "Late" in attendance_status:
                color = (0, 255, 255)  # Yellow
            else:
                color = (0, 0, 255)  # Red for not registered
            
            # Draw face rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw labels
            label = "Unknown Person" if name == "Unknown" else name
            cv2.rectangle(frame, (left, bottom - 60), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 35), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, attendance_status, (left + 6, bottom - 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)
        
        # ==================== SYSTEM STATUS DISPLAY ====================
        current_time = datetime.now().time()
        
        # Performance indicator
        perf_text = f"Performance: Processing every {FRAME_SKIP} frames | Frame: {frame_count}"
        cv2.putText(frame, perf_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        # Time and system info
        time_text = f"Time: {current_time.strftime('%H:%M:%S')} | Reporting: {REPORTING_TIME.strftime('%H:%M')}"
        cv2.putText(frame, time_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Attendance count
        count_text = f"Registered: {len(known_face_names)} | Marked Today: {len(attendance_today)}"
        cv2.putText(frame, count_text, (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Controls
        controls_text = "Press: 'q'=Quit | 's'=Add Person | 'r'=Reload | 'v'=Report"
        cv2.putText(frame, controls_text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        cv2.imshow('🎓 Attendance System', frame)
        
        # ==================== KEY CONTROLS ====================
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Add single person manually
            new_encoding, new_name = load_single_face()
            if new_encoding is not None:
                known_face_encodings.append(new_encoding)
                known_face_names.append(new_name)
                print(f"➕ Added {new_name} to system (temporary - add to Pics folder for permanent)")
        elif key == ord('r'):
            # Reload faces from Pics folder
            print(f"\n🔄 Reloading faces from '{PICS_FOLDER}' folder...")
            new_encodings, new_names = load_faces_from_pics_folder()
            if new_encodings:
                known_face_encodings = new_encodings
                known_face_names = new_names
                print(f"🔄 Reloaded {len(new_encodings)} faces from '{PICS_FOLDER}'")
            else:
                print(f"⚠️  No faces found in '{PICS_FOLDER}' folder")
        elif key == ord('v'):
            # Show attendance report
            print(f"\n📊 ATTENDANCE REPORT - {datetime.now().strftime('%Y-%m-%d')}")
            print(f"📁 File: {get_attendance_filename()}")
            if os.path.exists(get_attendance_filename()):
                with open(get_attendance_filename(), 'r') as file:
                    print(file.read())
            else:
                print("No attendance records for today.")
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Final report
    print(f"\n🎯 ATTENDANCE SESSION COMPLETED")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"👥 Total Registered: {len(known_face_names)}")
    print(f"✅ Marked Today: {len(attendance_today)}")
    print(f"📄 Records saved to: {get_attendance_filename()}")
    print(f"📸 Photos folder: {PICS_FOLDER}/")
    print(f"💡 To add new people: Add photos to '{PICS_FOLDER}' folder")

if __name__ == "__main__":
    main()

