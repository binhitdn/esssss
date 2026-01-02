#!/usr/bin/env python3
"""
Test script để kiểm tra và sửa lỗi hệ thống đánh thức
"""
import sys
import os

def test_wakeup_imports():
    """Test các import cần thiết cho wakeup system"""
    print("🔍 Kiểm tra imports...")
    
    try:
        import discord
        print("✅ discord.py - OK")
    except ImportError as e:
        print(f"❌ discord.py - FAILED: {e}")
        return False
    
    try:
        import asyncio
        print("✅ asyncio - OK")
    except ImportError as e:
        print(f"❌ asyncio - FAILED: {e}")
        return False
    
    try:
        import time
        print("✅ time - OK")
    except ImportError as e:
        print(f"❌ time - FAILED: {e}")
        return False
    
    try:
        from datetime import datetime, timedelta
        import pytz
        print("✅ datetime & pytz - OK")
    except ImportError as e:
        print(f"❌ datetime/pytz - FAILED: {e}")
        return False
    
    return True

def test_bot_syntax():
    """Test syntax của bot file"""
    print("\n🔍 Kiểm tra syntax bot file...")
    
    try:
        import ast
        with open('leaderboard_only_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        ast.parse(content)
        print("✅ Bot syntax - OK")
        return True
    except SyntaxError as e:
        print(f"❌ Bot syntax - FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ Bot file error: {e}")
        return False

def check_wakeup_commands():
    """Kiểm tra các lệnh đánh thức trong bot file"""
    print("\n🔍 Kiểm tra wakeup commands...")
    
    try:
        with open('leaderboard_only_bot.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        wakeup_commands = [
            'name="danh-thuc"',
            'name="danh-thuc-user"',
            'name="danh-thuc-kenh"',
            'name="danh-thuc-hen-gio"',
            'name="danh-thuc-pomodoro"',
            'name="danh-thuc-stats"'
        ]
        
        for cmd in wakeup_commands:
            if cmd in content:
                print(f"✅ {cmd} - Found")
            else:
                print(f"❌ {cmd} - Missing")
                return False
        
        # Kiểm tra hàm wakeup_command
        if 'async def wakeup_command(' in content:
            print("✅ wakeup_command function - Found")
        else:
            print("❌ wakeup_command function - Missing")
            return False
        
        # Kiểm tra generate_wakeup_content
        if 'async def generate_wakeup_content(' in content:
            print("✅ generate_wakeup_content function - Found")
        else:
            print("❌ generate_wakeup_content function - Missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking commands: {e}")
        return False

def check_config():
    """Kiểm tra config files"""
    print("\n🔍 Kiểm tra config files...")
    
    config_files = [
        'config/secrets.conf',
        'config/bot.conf'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} - Exists")
        else:
            print(f"❌ {config_file} - Missing")
            return False
    
    return True

def check_sync_status():
    """Kiểm tra trạng thái sync commands"""
    print("\n🔍 Kiểm tra sync status...")
    
    if os.path.exists('.sync_commands'):
        print("✅ .sync_commands flag - Exists (commands will be synced on next startup)")
    else:
        print("⚠️ .sync_commands flag - Missing (commands may not be synced)")
    
    if os.path.exists('sync_commands.py'):
        print("✅ sync_commands.py - Exists")
    else:
        print("❌ sync_commands.py - Missing")
        return False
    
    return True

def suggest_fixes():
    """Đề xuất cách sửa lỗi"""
    print("\n🔧 ĐỀ XUẤT SỬA LỖI:")
    print("=" * 50)
    
    print("\n1. 🔄 SYNC COMMANDS:")
    print("   python3 sync_commands.py")
    print("   → Tạo flag để sync commands lần khởi động tiếp theo")
    
    print("\n2. 🚀 KHỞI ĐỘNG BOT:")
    print("   python3 start.py")
    print("   → Bot sẽ tự động sync commands nếu có flag")
    
    print("\n3. ⏰ ĐỢI DISCORD CẬP NHẬT:")
    print("   Đợi 1-2 phút sau khi khởi động bot")
    print("   → Discord cần thời gian cập nhật slash commands")
    
    print("\n4. 🧪 TEST COMMANDS:")
    print("   Thử gõ / trong Discord và tìm 'danh-thuc'")
    print("   → Nếu không thấy, có thể cần sync lại")
    
    print("\n5. 🔍 KIỂM TRA PERMISSIONS:")
    print("   Bot cần quyền:")
    print("   - Send Messages")
    print("   - Use Slash Commands")
    print("   - Mention Everyone (cho /danh-thuc)")
    
    print("\n6. 📋 KIỂM TRA LOGS:")
    print("   Xem logs khi khởi động bot để tìm lỗi")
    print("   → Tìm dòng 'Đã sync X slash commands'")

def main():
    """Hàm main"""
    print("🔧 WAKEUP SYSTEM DIAGNOSTIC TOOL")
    print("=" * 50)
    
    all_good = True
    
    # Test imports
    if not test_wakeup_imports():
        all_good = False
    
    # Test syntax
    if not test_bot_syntax():
        all_good = False
    
    # Check commands
    if not check_wakeup_commands():
        all_good = False
    
    # Check config
    if not check_config():
        all_good = False
    
    # Check sync
    if not check_sync_status():
        all_good = False
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("✅ TẤT CẢ KIỂM TRA PASSED!")
        print("\n💡 Nếu commands vẫn không hoạt động:")
        print("1. Khởi động bot: python3 start.py")
        print("2. Đợi 1-2 phút")
        print("3. Thử lại commands trong Discord")
    else:
        print("❌ CÓ LỖI ĐƯỢC PHÁT HIỆN!")
        suggest_fixes()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Sửa các lỗi (nếu có)")
    print("2. Chạy: python3 sync_commands.py")
    print("3. Khởi động bot: python3 start.py")
    print("4. Test commands trong Discord")

if __name__ == "__main__":
    main()