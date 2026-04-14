#!/usr/bin/env python3
"""
GPS Integration Test Script
Tests the GPS location logging functionality
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_GPS_DATA = {
    "latitude": 37.7749,  # San Francisco coordinates
    "longitude": -122.4194,
    "accuracy": 10.5
}

def test_gps_attendance():
    """Test GPS attendance marking"""
    print("🧪 Testing GPS Attendance Integration")
    print("=" * 50)
    
    # Test 1: Try to mark attendance without pending recognition
    print("1. Testing attendance without pending recognition...")
    response = requests.post(f"{BASE_URL}/api/mark_attendance_with_gps", 
                           json=TEST_GPS_DATA)
    
    if response.status_code == 200:
        data = response.json()
        if not data['success']:
            print("✅ Correctly rejected - no pending attendance")
        else:
            print("❌ Should have rejected - no pending attendance")
    else:
        print(f"❌ Request failed with status {response.status_code}")
    
    # Test 2: Check recent attendance API
    print("\n2. Testing recent attendance API...")
    response = requests.get(f"{BASE_URL}/api/recent_attendance")
    
    if response.status_code == 401:
        print("✅ Correctly requires admin authentication")
    else:
        print(f"❌ Should require authentication, got status {response.status_code}")
    
    print("\n🎯 GPS Integration Test Complete!")
    print("📝 Manual testing required:")
    print("   1. Start the camera in employee mode")
    print("   2. Show a known face to trigger recognition")
    print("   3. Check that GPS location is automatically captured")
    print("   4. Verify location appears in admin dashboard")

if __name__ == "__main__":
    test_gps_attendance()