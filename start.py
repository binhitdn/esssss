#!/usr/bin/env python3
"""
StudyLion Leaderboard Bot Starter
Chạy toàn bộ project với GUI và Bot
"""
import subprocess
import sys
import os
import time
import signal
import threading

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết"""
    print("🔍 Kiểm tra yêu cầu...")
    
    # Kiểm tra virtual environment
    if not os.path.exists('venv'):
        print("❌ Không tìm thấy virtual environment!")
        print("💡 Hãy tạo venv trước: python3 -m venv venv")
        return False
    
    # Kiểm tra token
    if not os.path.exists('config/secrets.conf'):
        print("❌ Không tìm thấy config/secrets.conf!")
        print("💡 Tạo file này với nội dung:")
        print("[STUDYLION]")
        print("token = your_bot_token_here")
        return False
    
    # Kiểm tra token có được cấu hình không
    try:
        with open('config/secrets.conf', 'r') as f:
            content = f.read()
            if 'token =' not in content:
                print("❌ Token chưa được cấu hình trong secrets.conf!")
                return False
    except:
        print("❌ Không thể đọc config/secrets.conf!")
        return False
    
    print("✅ Cấu hình OK")
    return True

def cleanup_old_processes():
    """Dọn dẹp process cũ"""
    print("🧹 Dọn dẹp process cũ...")
    
    try:
        # Kill old processes
        subprocess.run(['pkill', '-f', 'leaderboard_only_bot.py'], 
                      capture_output=True, check=False)
        subprocess.run(['pkill', '-f', 'start_gui.py'], 
                      capture_output=True, check=False)
        
        # Remove old socket
        if os.path.exists('gui.sock'):
            os.remove('gui.sock')
            
    except Exception as e:
        print(f"⚠️ Lỗi dọn dẹp: {e}")

def start_gui_server():
    """Khởi động GUI server"""
    print("🎨 Khởi động GUI server...")
    
    # Dọn dẹp socket cũ nếu có (double check)
    if os.path.exists('gui.sock'):
        try:
            os.remove('gui.sock')
        except:
            pass
    
    try:
        process = subprocess.Popen([
            'venv/bin/python', 'scripts/start_gui.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Đợi GUI server khởi động
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ GUI server đã khởi động (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ GUI server lỗi: {stdout.decode()}") # stderr merged to stdout
            return None
            
    except Exception as e:
        print(f"❌ Không thể khởi động GUI: {e}")
        return None



def ensure_logs_dir():
    """Đảm bảo thư mục logs tồn tại"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("📁 Đã tạo thư mục logs")

def start_bot():
    """Khởi động bot"""
    print("🏆 Khởi động leaderboard bot...")
    
    ensure_logs_dir()
    
    try:
        # Use append mode and line buffering
        log_file = open('logs/bot_debug.log', 'a', buffering=1)
        # Write a separator for new run
        log_file.write(f"\n{'='*20} RESTART {time.strftime('%Y-%m-%d %H:%M:%S')} {'='*20}\n")
        
        process = subprocess.Popen([
            'venv/bin/python', '-u', 'leaderboard_only_bot.py'
        ], stdout=log_file, stderr=subprocess.STDOUT)
        
        # Đợi bot khởi động
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ Bot đã khởi động (PID: {process.pid})")
            return process, log_file
        else:
            print("❌ Bot không khởi động được!")
            return None, log_file
            
    except Exception as e:
        print(f"❌ Không thể khởi động bot: {e}", file=sys.stderr)
        return None, None

def monitor_output(process, name):
    """Theo dõi output của process"""
    try:
        while True:
            line = process.stdout.readline()
            if line:
                print(f"[{name}] {line.decode().strip()}")
            elif process.poll() is not None:
                break
            time.sleep(0.1)
    except:
        pass

def main():
    """Main function"""
    print("🚀 Khởi động StudyLion Leaderboard Bot")
    print("=" * 40)
    
    # Kiểm tra yêu cầu
    if not check_requirements():
        return 1
    
    # Dọn dẹp process cũ
    cleanup_old_processes()
    
    # Khởi động GUI server
    gui_process = start_gui_server()
    if not gui_process:
        print("❌ Không thể khởi động GUI server!")
        return 1
    
    # Khởi động bot
    bot_process, bot_log_file = start_bot()
    if not bot_process:
        print("❌ Không thể khởi động bot!")
        if gui_process:
            gui_process.terminate()
        return 1
    
    print("")
    print("🎉 KHỞI ĐỘNG THÀNH CÔNG!")
    print("=" * 40)
    print("🏆 Chức năng: Bảng xếp hạng từ API")
    print("🎯 Server: 1434581250798125068")
    print("📊 GUI: ✅ Có")
    print("📡 API: http://192.168.128.173:3001")
    print("")
    print("📋 Lệnh Discord:")
    print("   /bangxephang - Bảng xếp hạng hôm nay")
    print("   /bangxephang-tuan - Bảng xếp hạng tuần này")
    print("   /bangxephang-thang - Bảng xếp hạng tháng này")
    print("")
    print("⌨️ Nhấn Ctrl+C để dừng")
    print("=" * 40)
    
    # Bắt đầu theo dõi output
    gui_thread = threading.Thread(target=monitor_output, args=(gui_process, "GUI"))
    # bot_thread = threading.Thread(target=monitor_output, args=(bot_process, "BOT"))
    
    gui_thread.daemon = True
    # bot_thread.daemon = True
    
    gui_thread.start()
    # bot_thread.start()
    
    # Function cleanup khi thoát
    def cleanup():
        print("\n🛑 Đang tắt...")
        
        # Tắt bot
        if bot_process and bot_process.poll() is None:
            bot_process.terminate()
            try:
                bot_process.wait(timeout=5)
                print("✅ Đã tắt bot")
            except subprocess.TimeoutExpired:
                bot_process.kill()
                print("✅ Đã force kill bot")
        
        # Tắt GUI
        if gui_process and gui_process.poll() is None:
            gui_process.terminate()
            try:
                gui_process.wait(timeout=5)
                print("✅ Đã tắt GUI server")
            except subprocess.TimeoutExpired:
                gui_process.kill()
                print("✅ Đã force kill GUI server")
        
        # Dọn dẹp
        if os.path.exists('gui.sock'):
            os.remove('gui.sock')
        
        print("✅ Dọn dẹp hoàn tất")
    
    # Bắt signal Ctrl+C
    def signal_handler(signum, frame):
        cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Theo dõi process
    try:
        while True:
            # Kiểm tra bot còn chạy không
            if bot_process.poll() is not None:
                print("⚠️ Bot đã dừng!")
                cleanup()
                return 1
            
            # Kiểm tra GUI còn chạy không
            if gui_process.poll() is not None:
                print("⚠️ GUI server đã dừng!")
                cleanup()
                return 1
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        cleanup()
        return 0

if __name__ == '__main__':
    sys.exit(main())