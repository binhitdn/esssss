
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
        print("📤 Sending test LEADERBOARD request...")
        
        # Prepare sample data for leaderboard
        # Structure: (userid, position, time, name, avatar_key)
        sample_entries = [
            (123456789, 1, 3600 * 10, "User One", (0, None)),
            (987654321, 2, 3600 * 5, "User Two", (0, None)),
            (456123789, 3, 3600 * 2, "User Three", (0, None))
        ]
        
        # Request arguments matching LeaderboardCard signature
        # kwargs needs: server_name, entries, highlight
        kwargs = {
            'server_name': 'Debug Server',
            'entries': sample_entries,
            'highlight': None,
            'locale': 'vi'
        }
        
        # Send request
        response = await client.request('leaderboard_card', args=(), kwargs=kwargs)
        
        if response:
            print(f"✅ Render successful! Received {len(response)} bytes of image data.")
            with open('debug_render_output.png', 'wb') as f:
                f.write(response)
            print("🖼️ Saved output to 'debug_render_output.png'")
        else:
            print("❌ Render returned header/empty response.")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
