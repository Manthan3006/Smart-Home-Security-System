#!/usr/bin/env python3
"""
🎓 HOME SECURITY SYSTEM LAUNCHER
Launch script for the modern glassmorphism home security system
"""

import sys
import os
import subprocess
import importlib.util

def check_and_install_requirements():
    """Check and install required packages"""
    required_packages = [
        'customtkinter',
        'opencv-python', 
        'face-recognition',
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
        'Pillow'
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

def main():
    """Main launcher function"""
    print("🎓 Home Security System")
    print("=" * 50)
    
    # Check requirements
    if not check_and_install_requirements():
        print("Please install required packages and try again.")
        return
    
    # Import and run the home security system
    try:
        from home_security_ui import HomeSecurityUI
        
        print("🚀 Starting Home Security System...")
        print("Features:")
        print("  ✨ Glassmorphism UI Design")
        print("  📊 Admin Analytics Dashboard")
        print("  👥 Employee Statistics")
        print("  📷 Real-time Face Recognition")
        print("  🔐 Secure Admin Access")
        print("\n🎯 Default Admin Password: admin123")
        print("=" * 50)
        
        # Start the application
        app = HomeSecurityUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importing home security system: {e}")
        print("Please ensure home_security_ui.py is in the same directory.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()