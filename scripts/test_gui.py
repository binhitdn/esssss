#!/usr/bin/env python3
"""
Test script to check if GUI rendering is working properly.
"""
import sys
import os
import asyncio
import subprocess
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_gui():
    """Test GUI server functionality"""
    print("🧪 Testing GUI server...")
    
    # Start GUI server
    print("1️⃣ Starting GUI server...")
    gui_process = subprocess.Popen([
        sys.executable, "scripts/start_gui.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    await asyncio.sleep(3)
    
    if gui_process.poll() is not None:
        stdout, stderr = gui_process.communicate()
        print(f"❌ GUI server failed:")
        print(f"STDOUT: {stdout.decode()}")
        print(f"STDERR: {stderr.decode()}")
        return False
    
    print("✅ GUI server started")
    
    # Test GUI client connection
    print("2️⃣ Testing GUI client connection...")
    try:
        from gui.client import client
        
        # Try a ping request
        try:
            result = await client.request('ping', timeout=5)
            if result == b"Pong":
                print("✅ GUI client can connect to server")
                success = True
            else:
                print(f"❌ Unexpected ping response: {result}")
                success = False
        except Exception as e:
            print(f"❌ GUI client connection failed: {e}")
            success = False
    except Exception as e:
        print(f"❌ GUI client import failed: {e}")
        success = False
    
    # Cleanup
    print("3️⃣ Cleaning up...")
    gui_process.terminate()
    try:
        gui_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        gui_process.kill()
    
    # Remove socket file
    socket_path = Path("gui.sock")
    if socket_path.exists():
        socket_path.unlink()
    
    return success

def main():
    print("🎨 StudyLion GUI Test")
    print("=" * 30)
    
    try:
        result = asyncio.run(test_gui())
        if result:
            print("\n🎉 GUI system is working!")
            print("✅ You can now use /leaderboard and other image commands")
        else:
            print("\n❌ GUI system has issues")
            print("🔧 Check the error messages above")
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
        return 1

if __name__ == '__main__':
    sys.exit(main())