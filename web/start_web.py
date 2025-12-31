#!/usr/bin/env python3
"""
StudyLion Web Dashboard Starter
Khởi động web server độc lập
"""
import subprocess
import sys
import os
import time

def check_requirements():
    """Kiểm tra các yêu cầu cần thiết"""
    print("🔍 Kiểm tra yêu cầu web server...")
    
    # Kiểm tra virtual environment
    if not os.path.exists('../venv'):
        print("❌ Không tìm thấy virtual environment!")
        print("💡 Hãy tạo venv trước: python3 -m venv venv")
        return False
    
    # Kiểm tra Flask đã cài chưa
    try:
        result = subprocess.run(['../venv/bin/python', '-c', 'import flask, discord'], 
                              capture_output=True, check=True)
        print("✅ Flask và Discord.py đã sẵn sàng")
    except subprocess.CalledProcessError:
        print("⚠️ Dependencies chưa được cài đặt, đang cài...")
        try:
            subprocess.run(['../venv/bin/pip', 'install', '-r', 'requirements.txt'], 
                          check=True)
            print("✅ Đã cài đặt dependencies")
        except subprocess.CalledProcessError:
            print("❌ Không thể cài đặt dependencies!")
            return False
    
    return True

def start_web_server():
    """Khởi động web server"""
    print("🌐 Khởi động StudyLion Web Dashboard...")
    
    try:
        # Chạy Flask app
        process = subprocess.Popen([
            '../venv/bin/python', 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print("✅ Web server đã khởi động!")
        print("=" * 50)
        print("🌐 URL: http://localhost:5001")
        print("📊 Dashboard: Thống kê server Discord")
        print("🔄 Auto refresh: 30 giây")
        print("⌨️ Nhấn Ctrl+C để dừng")
        print("=" * 50)
        
        # Theo dõi output
        try:
            while True:
                line = process.stdout.readline()
                if line:
                    print(line.strip())
                elif process.poll() is not None:
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Đang tắt web server...")
            process.terminate()
            try:
                process.wait(timeout=5)
                print("✅ Đã tắt web server")
            except subprocess.TimeoutExpired:
                process.kill()
                print("✅ Đã force kill web server")
                
    except Exception as e:
        print(f"❌ Không thể khởi động web server: {e}")
        return 1
    
    return 0

def main():
    """Main function"""
    print("🚀 StudyLion Web Dashboard Starter")
    print("=" * 40)
    
    # Kiểm tra yêu cầu
    if not check_requirements():
        return 1
    
    # Khởi động web server
    return start_web_server()

if __name__ == '__main__':
    sys.exit(main())