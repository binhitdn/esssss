#!/usr/bin/env python3
"""
Test GUI trực tiếp với leaderboard
"""
import asyncio
import aiohttp
import pickle
import os

async def test_direct():
    """Test trực tiếp"""
    print("🧪 Test GUI trực tiếp...")
    
    if not os.path.exists('gui.sock'):
        print("❌ gui.sock không tồn tại")
        return False
    
    # Dữ liệu test đơn giản
    entries = [
        (1, 1, 18600, "Nguyen Van An", (0, None)),
        (2, 2, 17240, "Tran Thi Mai", (0, None)),
        (3, 3, 16530, "Le Hoang Minh", (0, None))
    ]
    
    gui_data = {
        'server_name': 'Test Server',
        'entries': entries,
        'highlight': None
    }
    
    try:
        request_data = pickle.dumps(('leaderboard_card', [], gui_data))
        
        connector = aiohttp.UnixConnector(path='gui.sock')
        
        async with aiohttp.ClientSession(connector=connector) as session:
            print("📡 Gửi request...")
            async with session.post('http://localhost/', data=request_data) as resp:
                print(f"📊 Response status: {resp.status}")
                
                if resp.status == 200:
                    data = await resp.read()
                    print(f"✅ Thành công! Kích thước: {len(data)} bytes")
                    
                    with open('test_output.png', 'wb') as f:
                        f.write(data)
                    print("💾 Đã lưu: test_output.png")
                    return True
                else:
                    error = await resp.text()
                    print(f"❌ Lỗi: {error}")
                    return False
                    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_direct())
    print("🎯 Kết quả:", "✅ Thành công" if success else "❌ Thất bại")