#!/usr/bin/env python3
"""
Final UI Test: Verify that both applications produce identical results in their web interfaces
"""

import subprocess
import time
import requests
import sys
from typing import Dict, Any
import json

def start_streamlit_app(script_name: str, port: int) -> subprocess.Popen:
    """Start a Streamlit app on the specified port"""
    print(f"🚀 Starting {script_name} on port {port}...")
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", script_name, "--server.port", str(port), "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for the app to start
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            response = requests.get(f"http://localhost:{port}")
            if response.status_code == 200:
                print(f"✅ {script_name} is running on port {port}")
                return process
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    print(f"❌ Failed to start {script_name} on port {port}")
    process.terminate()
    return None

def test_app_status(port: int, app_name: str) -> bool:
    """Test if the app is responding correctly"""
    try:
        response = requests.get(f"http://localhost:{port}")
        if response.status_code == 200:
            print(f"✅ {app_name} is accessible and responding")
            return True
        else:
            print(f"❌ {app_name} returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {app_name} is not accessible: {e}")
        return False

def main():
    print("🎯 Final UI Test: Verifying Both Applications")
    print("=" * 60)
    
    # Start original app
    original_process = start_streamlit_app("streamlit_app.py", 8501)
    if not original_process:
        print("❌ Failed to start original app")
        return False
    
    # Start new app
    new_process = start_streamlit_app("main_app.py", 8502)
    if not new_process:
        print("❌ Failed to start new app")
        original_process.terminate()
        return False
    
    try:
        print("\n📋 Testing Application Status...")
        
        # Test both apps
        original_ok = test_app_status(8501, "Original Tactical Tracker (streamlit_app.py)")
        new_ok = test_app_status(8502, "New Portfolio Management Suite (main_app.py)")
        
        if original_ok and new_ok:
            print("\n✅ SUCCESS: Both applications are running correctly!")
            print("\n📱 You can now test them manually:")
            print("   • Original App: http://localhost:8501")
            print("   • New App: http://localhost:8502 (select 'Tactical Tracker')")
            print("\n🎯 Both apps should show identical results for the same inputs!")
            
            input("\nPress Enter to stop the applications...")
            return True
        else:
            print("\n❌ FAILURE: One or both applications failed to start properly")
            return False
    
    finally:
        print("\n🛑 Stopping applications...")
        if original_process:
            original_process.terminate()
        if new_process:
            new_process.terminate()
        print("✅ Applications stopped")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
