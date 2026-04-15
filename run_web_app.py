#!/usr/bin/env python3
"""
🎓 HOME SECURITY SYSTEM - WEB APPLICATION LAUNCHER
Professional Flask-based home security management system
"""

import sys
import os
import subprocess
import importlib.util

def check_and_install_requirements():
    """Check and install required packages"""
    required_packages = [
        'flask',
        'opencv-python', 
        'face-recognition',
        'pandas',
        'matplotlib',
        'seaborn',
        'Pillow',
        'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'face-recognition':
                import face_recognition
            elif package == 'Pillow':
                import PIL
            else:
                importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("🔧 Installing missing packages...")
        print(f"Missing: {', '.join(missing_packages)}")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install'
            ] + missing_packages)
            print("✅ All packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['Pics', 'attendance_records', 'static/images']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def check_face_images():
    """Check if face images exist"""
    pics_folder = 'Pics'
    if not os.path.exists(pics_folder):
        return False
    
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [f for f in os.listdir(pics_folder) 
                   if f.lower().endswith(supported_extensions)]
    
    return len(image_files) > 0

def main():
    """Main launcher function"""
    print("🏠 Home Security System - Web Application")
    print("=" * 60)
    print("🌐 Modern Flask-based home security management")
    print("✨ Features:")
    print("  • Glassmorphism UI Design")
    print("  • Real-time Face Recognition")
    print("  • Admin Analytics Dashboard")
    print("  • Person Statistics")
    print("  • Secure Role-based Access")
    print("=" * 60)
    
    # Check requirements
    print("🔍 Checking requirements...")
    if not check_and_install_requirements():
        print("Please install required packages and try again.")
        return
    
    # Setup directories
    print("📁 Setting up directories...")
    setup_directories()
    
    # Check for face images
    if not check_face_images():
        print("\n⚠️  No face images found in 'Pics' folder!")
        print("📸 Please add employee photos to the 'Pics' folder:")
        print("   • Supported formats: JPG, PNG, BMP, GIF")
        print("   • Filename = Employee name (e.g., 'john_doe.jpg')")
        print("   • Use clear, front-facing photos")
        print("\n🚀 You can still run the system - add photos later and restart")
    
    # Import and run the Flask app
    try:
        print("\n🚀 Starting Flask web server...")
        print("📱 Access the application at:")
        print("   🌐 http://127.0.0.1:8000")
        print("   (Navigate to Employee or Admin sections from the home page)")
        print("\n🔐 Default Admin Credentials:")
        print("   • Password: admin123")
        print("\n💡 Tips:")
        print("   • Use Chrome/Firefox for best experience")
        print("   • Allow camera access when prompted")
        print("   • Ensure good lighting for face recognition")
        print("=" * 60)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='127.0.0.1', port=8000, threaded=True)
        
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("Please ensure app.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()