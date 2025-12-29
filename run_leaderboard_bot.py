#!/usr/bin/env python3
"""
Chạy Bot Bảng Xếp Hạng - Chỉ có chức năng bảng xếp hạng
"""
import subprocess
import sys
import os
import time
import signal

def check_token():
    """Kiểm tra token có tồn tại không"""
    if not os.path.exists('config/secrets.conf'):
        print("❌ Không tìm thấy config/secrets.conf")
        print("💡 Tạo file này với nội dung:")
        print("[STUDYLION]")
        print("token = your_bot_token_here")
        return False
    
    with open('config/secrets.conf', 'r') as f:
        content = f.read()
        if 'token =' in content:
            print("✅ Token đã được cấu hình")
            return True
        else:
            print("❌ Token chưa được cấu hình trong secrets.conf")
            return False

def start_gui_server():
    """Khởi động GUI server"""
    print("🎨 Khởi động GUI server...")
    try:
        gui_process = subprocess.Popen([
            sys.executable, "scripts/start_gui.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đợi một chút
        time.sleep(3)
        
        if gui_process.poll() is None:
            print("✅ GUI server đã khởi động")
            return gui_process
        else:
            stdout, stderr = gui_process.communicate()
            print(f"❌ GUI server lỗi: {stderr.decode()[:200]}")
            return None
    except Exception as e:
        print(f"❌ Không thể khởi động GUI: {e}")
        return None

def start_bot():
    """Khởi động bot bảng xếp hạng"""
    print("🏆 Khởi động bot bảng xếp hạng...")
    try:
        bot_process = subprocess.Popen([
            sys.executable, "leaderboard_only_bot.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        print("✅ Bot đã khởi động")
        return bot_process
    except Exception as e:
        print(f"❌ Không thể khởi động bot: {e}")
        return None

def main():
    """Main function"""
    print("🚀 Bot Bảng Xếp Hạng")
    print("=" * 30)
    
    # Kiểm tra token
    if not check_token():
        return 1
    
    # Khởi động GUI server
    gui_process = start_gui_server()
    if not gui_process:
        print("⚠️ Tiếp tục mà không có GUI (chỉ text)")
    
    # Khởi động bot
    bot_process = start_bot()
    if not bot_process:
        print("❌ Không thể khởi động bot")
        if gui_process:
            gui_process.terminate()
        return 1
    
    print("\n🎉 BOT ĐÃ KHỞI ĐỘNG!")
    print("=" * 30)
    print("🏆 Chức năng: Chỉ bảng xếp hạng")
    print("🎯 Server: 1434581250798125068")
    print("📊 GUI:", "✅ Có" if gui_process else "❌ Không")
    print("\n📋 Lệnh Discord:")
    print("   /bangxephang - Bảng xếp hạng")
    print("\n⌨️ Nhấn Ctrl+C để dừng")
    print("=" * 30)
    
    # Theo dõi bot
    try:
        while True:
            # Hiển thị output của bot
            line = bot_process.stdout.readline()
            if line:
                print(line.decode().strip())
            
            # Kiểm tra bot còn chạy không
            if bot_process.poll() is not None:
                print("⚠️ Bot đã dừng")
                break
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n🛑 Đang tắt...")
        
        # Tắt bot
        if bot_process:
            bot_process.terminate()
            try:
                bot_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                bot_process.kill()
        
        # Tắt GUI
        if gui_process:
            gui_process.terminate()
            try:
                gui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gui_process.kill()
        
        # Dọn dẹp
        if os.path.exists('gui.sock'):
            os.remove('gui.sock')
        
        print("✅ Đã tắt hoàn tất")
        return 0

if __name__ == '__main__':
    sys.exit(main())