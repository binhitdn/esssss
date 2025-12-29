#!/usr/bin/env python3
"""
Test GUI với client gốc của LionBot
"""
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

async def test_gui_client():
    """Test GUI client"""
    print("🧪 Test GUI Client...")
    
    if not os.path.exists('gui.sock'):
        print("❌ GUI server chưa chạy")
        return False
    
    try:
        from gui.client import client as gui_client
        
        # Test ping trước
        print("🏓 Test ping...")
        ping_result = await gui_client.request('ping')
        print(f"✅ Ping OK: {ping_result}")
        
        # Test leaderboard
        print("📊 Test leaderboard...")
        entries = [
            (1, 1, 18600, "Nguyen Van An", (0, None)),
            (2, 2, 17240, "Tran Thi Mai", (0, None)),
            (3, 3, 16530, "Le Hoang Minh", (0, None)),
            (4, 4, 15420, "Pham Quoc Bao", (0, None)),
            (5, 5, 14890, "Vo Thanh Dat", (0, None))
        ]
        
        image_data = await gui_client.request(
            route='leaderboard_card',
            args=(),
            kwargs={
                'server_name': '14 hours a day(STUDY VIP)',
                'entries': entries,
                'highlight': None,
                'locale': 'vi'
            }
        )
        
        print(f"✅ Leaderboard OK: {len(image_data)} bytes")
        
        # Lưu ảnh
        with open('test_leaderboard_client.png', 'wb') as f:
            f.write(image_data)
        print("💾 Đã lưu: test_leaderboard_client.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main"""
    print("🚀 Test GUI Client - StudyLion")
    print("=" * 35)
    
    success = await test_gui_client()
    
    print("\n" + "=" * 35)
    if success:
        print("🎉 TEST THÀNH CÔNG!")
        print("✅ GUI client hoạt động tốt")
    else:
        print("❌ TEST THẤT BẠI")
        print("🔧 Kiểm tra GUI server")
    
    return success

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)