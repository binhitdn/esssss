#!/usr/bin/env python3
"""
Web Dashboard Setup
Script thiết lập web dashboard
"""
import os
import sys

def setup_config():
    """Thiết lập cấu hình web dashboard"""
    print("🔧 Thiết lập Web Dashboard")
    print("=" * 40)
    
    # Đọc cấu hình hiện tại
    config_file = 'config.py'
    current_server_id = None
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                if 'DISCORD_SERVER_ID' in line and '=' in line:
                    try:
                        current_server_id = line.split('=')[1].strip()
                        break
                    except:
                        pass
    
    print(f"Server ID hiện tại: {current_server_id}")
    print()
    
    # Nhập server ID mới
    while True:
        new_server_id = input("Nhập Discord Server ID mới (Enter để giữ nguyên): ").strip()
        
        if not new_server_id:
            if current_server_id:
                print("✅ Giữ nguyên cấu hình hiện tại")
                return
            else:
                print("❌ Cần nhập Server ID!")
                continue
        
        # Kiểm tra định dạng
        try:
            int(new_server_id)
            if len(new_server_id) < 15:
                print("❌ Server ID không hợp lệ (quá ngắn)")
                continue
            break
        except ValueError:
            print("❌ Server ID phải là số!")
            continue
    
    # Cập nhật config
    config_content = f'''#!/usr/bin/env python3
"""
Web Dashboard Configuration
Cấu hình cho web dashboard
"""

# Discord Server Configuration
DISCORD_SERVER_ID = {new_server_id}  # Server ID của bạn

# Web Server Configuration
WEB_HOST = '0.0.0.0'
WEB_PORT = 5001
DEBUG_MODE = True

# Cache Configuration
CACHE_DURATION = 300  # 5 phút (giây)

# Discord API Configuration
DISCORD_TOKEN_PATH = '../config/secrets.conf'

# Timezone
TIMEZONE = 'Asia/Ho_Chi_Minh'

# Server Display Name (nếu muốn override tên server)
SERVER_DISPLAY_NAME = None  # None = sử dụng tên thật từ Discord
'''
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"✅ Đã cập nhật Server ID: {new_server_id}")
    print()
    
    # Hướng dẫn tiếp theo
    print("📋 Các bước tiếp theo:")
    print("1. Đảm bảo bot token đã được cấu hình trong ../config/secrets.conf")
    print("2. Chạy web dashboard: python3 ../run_web_only.py")
    print("3. Truy cập: http://localhost:5001")
    print()
    print("🎯 Tính năng:")
    print("- Server Dashboard: Thống kê thành viên, roles, channels")
    print("- Leaderboard Demo: /leaderboard")
    print("- Advanced Analytics: /advanced")

def main():
    """Main function"""
    try:
        setup_config()
    except KeyboardInterrupt:
        print("\n❌ Đã hủy thiết lập")
        return 1
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())