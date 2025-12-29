#!/usr/bin/env python3
"""
Test script để kiểm tra bot tiếng Việt và GUI rendering
"""
import asyncio
import aiohttp
import json
import sys
import os

async def test_gui_server():
    """Test GUI server có hoạt động không"""
    print("🧪 Kiểm tra GUI server...")
    
    try:
        # Test basic GUI endpoint
        connector = aiohttp.UnixConnector(path='gui.sock')
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get('http://localhost/health') as resp:
                if resp.status == 200:
                    print("✅ GUI server đang hoạt động")
                    return True
                else:
                    print(f"❌ GUI server trả về status {resp.status}")
                    return False
    except Exception as e:
        print(f"❌ Không thể kết nối GUI server: {e}")
        return False

async def test_leaderboard_render():
    """Test render leaderboard"""
    print("🧪 Kiểm tra render leaderboard...")
    
    try:
        # Test data cho leaderboard
        test_data = {
            "title": "Bảng Xếp Hạng Học Tập",
            "members": [
                {"name": "Nguyễn Văn A", "time": "5h 30m", "rank": 1},
                {"name": "Trần Thị B", "time": "4h 15m", "rank": 2},
                {"name": "Lê Văn C", "time": "3h 45m", "rank": 3}
            ]
        }
        
        connector = aiohttp.UnixConnector(path='gui.sock')
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                'http://localhost/render/leaderboard',
                json=test_data
            ) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    if len(content) > 1000:  # Image should be reasonably sized
                        print("✅ Render leaderboard thành công")
                        print(f"📊 Kích thước ảnh: {len(content)} bytes")
                        return True
                    else:
                        print(f"❌ Ảnh quá nhỏ: {len(content)} bytes")
                        return False
                else:
                    error_text = await resp.text()
                    print(f"❌ Render thất bại: {resp.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Lỗi render leaderboard: {e}")
        return False

async def test_vietnamese_locale():
    """Test Vietnamese locale configuration"""
    print("🧪 Kiểm tra cấu hình tiếng Việt...")
    
    # Check if Vietnamese locale files exist
    base_po = "locales/vi/LC_MESSAGES/base_fixed.po"
    meta_po = "locales/vi/LC_MESSAGES/meta_fixed.po"
    
    if os.path.exists(base_po) and os.path.exists(meta_po):
        print("✅ File dịch tiếng Việt tồn tại")
        
        # Check content
        with open(base_po, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'trogiup' in content and 'bangxephang' in content:
                print("✅ Nội dung dịch tiếng Việt hợp lệ")
                return True
            else:
                print("❌ Nội dung dịch không đầy đủ")
                return False
    else:
        print("❌ Thiếu file dịch tiếng Việt")
        return False

def check_bot_status():
    """Kiểm tra bot có đang chạy không"""
    print("🧪 Kiểm tra trạng thái bot...")
    
    # Check if bot log shows it's online
    if os.path.exists('bot.log'):
        with open('bot.log', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'StudyLion initialised, starting!' in content:
                print("✅ Bot đã khởi động thành công")
                return True
    
    print("❌ Bot chưa khởi động hoặc có lỗi")
    return False

async def main():
    """Chạy tất cả tests"""
    print("🚀 Bắt đầu kiểm tra StudyLion Bot Tiếng Việt")
    print("=" * 50)
    
    results = []
    
    # Test 1: Bot status
    results.append(check_bot_status())
    
    # Test 2: Vietnamese locale
    results.append(await test_vietnamese_locale())
    
    # Test 3: GUI server
    gui_ok = await test_gui_server()
    results.append(gui_ok)
    
    # Test 4: Leaderboard rendering (only if GUI is working)
    if gui_ok:
        results.append(await test_leaderboard_render())
    else:
        print("⏭️ Bỏ qua test render vì GUI server không hoạt động")
        results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 KẾT QUẢ KIỂM TRA:")
    
    tests = [
        "Bot khởi động",
        "Tiếng Việt", 
        "GUI Server",
        "Render Leaderboard"
    ]
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {test}: {status}")
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n🎯 Tổng kết: {success_count}/{total_count} tests thành công")
    
    if success_count == total_count:
        print("🎉 TẤT CẢ TESTS ĐỀU THÀNH CÔNG!")
        print("🇻🇳 Bot tiếng Việt đã sẵn sàng sử dụng!")
    else:
        print("⚠️ Một số tests thất bại, cần kiểm tra lại")
    
    return success_count == total_count

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)