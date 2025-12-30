
import asyncio
import pickle
import sys
import os

# Adjust path to include src
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from gui.client import GUIclient

async def test_connection():
    print("--- Testing GUI Connection ---")
    
    # 1. Check if socket file exists
    if not os.path.exists('gui.sock'):
        print("❌ Error: 'gui.sock' does not exist. Is the GUI server running?")
        return

    print("✅ 'gui.sock' found.")

    # 2. Try to connect
    client = GUIclient(os.path.abspath('gui.sock'))
    print("📡 Connecting to GUI server...")
    
    try:
        # We'll try a dummy request or just a simple ping if available, 
        # but since there's no ping, we'll try a render request that might fail but verifies connection
        print("📤 Sending test request...")
        # Sending a request intended to fail fast or succeed
        # Using a non-existent route to check connectivity
        response = await client.request('ping_test', args=(), kwargs={})
        print(f"✅ Connection successful! Response: {response}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
