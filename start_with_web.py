#!/usr/bin/env python3
"""
StudyLion Full System Starter
Chạy Bot + GUI + Web Dashboard
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
    
    # Kiểm tra Flask
    try:
        subprocess.run(['venv/bin/python', '-c', 'import flask'], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Flask chưa được cài đặt, đang cài...")
        try:
            subprocess.run(['venv/bin/pip', 'install', '-r', 'web/requirements.txt'], 
                          check=True)
            print("✅ Đã cài đặt Flask")
        except subprocess.CalledProcessError:
            print("❌ Không thể cài đặt Flask!")
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
        subprocess.run(['pkill', '-f', 'web/app.py'], 
                      capture_output=True, check=False)
        
        # Remove old socket
        if os.path.exists('gui.sock'):
            os.remove('gui.sock')
            
    except Exception as e:
        print(f"⚠️ Lỗi dọn dẹp: {e}")

def start_gui_server():
    """Khởi động GUI server"""
    print("🎨 Khởi động GUI server...")
    
    if os.path.exists('gui.sock'):
        try:
            os.remove('gui.sock')
        except:
            pass
    
    try:
        process = subprocess.Popen([
            'venv/bin/python', 'scripts/start_gui.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ GUI server đã khởi động (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ GUI server lỗi: {stdout.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Không thể khởi động GUI: {e}")
        return None

def start_web_server():
    """Khởi động web server"""
    print("🌐 Khởi động web server...")
    
    try:
        process = subprocess.Popen([
            'venv/bin/python', 'web/app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.')
        
        time.sleep(2)
        
        if process.poll() is None:
            print(f"✅ Web server đã khởi động (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Web server lỗi: {stdout.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Không thể khởi động web server: {e}")
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
        log_file = open('logs/bot_debug.log', 'a', buffering=1)
        log_file.write(f"\n{'='*20} RESTART {time.strftime('%Y-%m-%d %H:%M:%S')} {'='*20}\n")
        
        process = subprocess.Popen([
            'venv/bin/python', '-u', 'leaderboard_only_bot.py'
        ], stdout=log_file, stderr=subprocess.STDOUT)
        
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
    print("🚀 Khởi động StudyLion Full System")
    print("=" * 50)
    
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
    
    # Khởi động web server
    web_process = start_web_server()
    if not web_process:
        print("❌ Không thể khởi động web server!")
        if gui_process:
            gui_process.terminate()
        return 1
    
    # Khởi động bot
    bot_process, bot_log_file = start_bot()
    if not bot_process:
        print("❌ Không thể khởi động bot!")
        if gui_process:
            gui_process.terminate()
        if web_process:
            web_process.terminate()
        return 1
    
    print("")
    print("🎉 KHỞI ĐỘNG THÀNH CÔNG!")
    print("=" * 50)
    print("🏆 Discord Bot: ✅ Hoạt động")
    print("🎨 GUI System: ✅ Hoạt động") 
    print("🌐 Web Dashboard: ✅ Hoạt động")
    print("")
    print("📋 Discord Commands:")
    print("   /bangxephang - Bảng xếp hạng hôm nay")
    print("   /bangxephang-tuan - Bảng xếp hạng tuần này")
    print("   /bangxephang-thang - Bảng xếp hạng tháng này")
    print("")
    print("🌐 Web Dashboard:")
    print("   URL: http://localhost:5001")
    print("   Features: Thống kê server, bảng xếp hạng")
    print("   Auto refresh: 30 giây")
    print("")
    print("⌨️ Nhấn Ctrl+C để dừng tất cả")
    print("=" * 50)
    
    # Bắt đầu theo dõi output
    gui_thread = threading.Thread(target=monitor_output, args=(gui_process, "GUI"))
    web_thread = threading.Thread(target=monitor_output, args=(web_process, "WEB"))
    
    gui_thread.daemon = True
    web_thread.daemon = True
    
    gui_thread.start()
    web_thread.start()
    
    # Function cleanup khi thoát
    def cleanup():
        print("\n🛑 Đang tắt tất cả services...")
        
        # Tắt bot
        if bot_process and bot_process.poll() is None:
            bot_process.terminate()
            try:
                bot_process.wait(timeout=5)
                print("✅ Đã tắt bot")
            except subprocess.TimeoutExpired:
                bot_process.kill()
                print("✅ Đã force kill bot")
        
        # Tắt web server
        if web_process and web_process.poll() is None:
            web_process.terminate()
            try:
                web_process.wait(timeout=5)
                print("✅ Đã tắt web server")
            except subprocess.TimeoutExpired:
                web_process.kill()
                print("✅ Đã force kill web server")
        
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
            
            # Kiểm tra web server còn chạy không
            if web_process.poll() is not None:
                print("⚠️ Web server đã dừng!")
                cleanup()
                return 1
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        cleanup()
        return 0

if __name__ == '__main__':
    sys.exit(main())