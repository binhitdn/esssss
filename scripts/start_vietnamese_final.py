#!/usr/bin/env python3
"""
StudyLion Bot Tiếng Việt - Phiên bản cuối cùng
Khởi động bot với đầy đủ tính năng tiếng Việt và GUI rendering
"""
import sys
import os
import asyncio
import subprocess
import time
import signal
from pathlib import Path

def setup_environment():
    """Thiết lập môi trường cho tiếng Việt"""
    os.environ['LANG'] = 'vi_VN.UTF-8'
    os.environ['LC_ALL'] = 'vi_VN.UTF-8'
    os.environ['STUDYLION_PRIVATE'] = '1'
    os.environ['STUDYLION_SINGLE_SERVER'] = '1434581250798125068'
    
    # Add src to Python path
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def cleanup_old_files():
    """Dọn dẹp các file cũ"""
    files_to_clean = ['gui.sock', 'bot.log']
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🧹 Đã xóa {file_path}")
            except:
                pass

def start_gui_server():
    """Khởi động GUI server"""
    print("🎨 Khởi động GUI server...")
    try:
        python_exe = sys.executable
        gui_process = subprocess.Popen([
            python_exe, "scripts/start_gui.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đợi GUI server khởi động
        time.sleep(3)
        
        if gui_process.poll() is None:
            print("✅ GUI server đã sẵn sàng")
            return gui_process
        else:
            stdout, stderr = gui_process.communicate()
            print(f"❌ GUI server lỗi: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Không thể khởi động GUI: {e}")
        return None

def start_bot():
    """Khởi động bot tiếng Việt"""
    print("🤖 Khởi động StudyLion Bot (Tiếng Việt)...")
    
    # Import bot directly
    try:
        from bot import _main as bot_main
        print("✅ Bot đã được import thành công")
        
        # Run bot in background thread
        import threading
        bot_thread = threading.Thread(target=bot_main, daemon=True)
        bot_thread.start()
        
        print("✅ Bot đang chạy trong background")
        return bot_thread
        
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")
        return None

def main():
    """Main function"""
    print("🚀 StudyLion Bot Tiếng Việt - Khởi động cuối cùng")
    print("=" * 55)
    
    # Setup
    setup_environment()
    cleanup_old_files()
    
    # Start GUI server
    gui_process = start_gui_server()
    if not gui_process:
        print("⚠️ GUI server không khởi động được, tiếp tục với bot...")
    
    # Start bot
    bot_thread = start_bot()
    if not bot_thread:
        print("❌ Không thể khởi động bot")
        return 1
    
    print("\n🎉 KHỞI ĐỘNG THÀNH CÔNG!")
    print("=" * 55)
    print("🇻🇳 Bot sử dụng tiếng Việt")
    print("🎯 Server ID: 1434581250798125068")
    print("📊 GUI rendering: " + ("✅ Có" if gui_process else "❌ Không"))
    print("\n📋 Các lệnh tiếng Việt có sẵn:")
    print("   /trogiup     - Xem trợ giúp")
    print("   /bangxephang - Bảng xếp hạng")
    print("   /dongho      - Timer pomodoro")
    print("   /toi         - Profile cá nhân")
    print("   /caidat      - Cấu hình bot")
    print("\n⌨️ Nhấn Ctrl+C để dừng bot")
    print("=" * 55)
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            
            # Check if bot thread is still alive
            if not bot_thread.is_alive():
                print("⚠️ Bot thread đã dừng")
                break
                
            # Check GUI process
            if gui_process and gui_process.poll() is not None:
                print("⚠️ GUI process đã dừng")
                gui_process = None
                
    except KeyboardInterrupt:
        print("\n🛑 Đang tắt bot...")
        
        # Cleanup
        if gui_process:
            gui_process.terminate()
            try:
                gui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                gui_process.kill()
        
        print("✅ Đã tắt hoàn tất")
        return 0

if __name__ == '__main__':
    sys.exit(main())