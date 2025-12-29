#!/usr/bin/env python3
"""
Khởi động StudyLion Bot hoàn chỉnh với tiếng Việt và GUI
"""
import sys
import os
import asyncio
import subprocess
import time
import signal
from pathlib import Path

class VietnameseBotManager:
    def __init__(self):
        self.gui_process = None
        self.bot_process = None
        self.running = True
        
    def signal_handler(self, signum, frame):
        print(f"\n🛑 Nhận tín hiệu {signum}, đang tắt bot...")
        self.running = False
        self.cleanup()
        
    def cleanup(self):
        """Tắt tất cả processes"""
        if self.gui_process:
            print("🔄 Đang tắt GUI server...")
            self.gui_process.terminate()
            try:
                self.gui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.gui_process.kill()
                
        if self.bot_process:
            print("🔄 Đang tắt bot...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
                
        # Dọn dẹp socket file
        socket_path = Path("gui.sock")
        if socket_path.exists():
            socket_path.unlink()
            
        print("✅ Đã tắt hoàn tất")
        
    def start_gui_server(self):
        """Khởi động GUI server"""
        print("🎨 Đang khởi động GUI server...")
        try:
            python_exe = sys.executable
            env = os.environ.copy()
            self.gui_process = subprocess.Popen([
                python_exe, "scripts/start_gui.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            
            # Đợi GUI server khởi động
            time.sleep(3)
            
            if self.gui_process.poll() is None:
                print("✅ GUI server đã khởi động thành công")
                return True
            else:
                stdout, stderr = self.gui_process.communicate()
                print(f"❌ GUI server không khởi động được:")
                print(f"STDOUT: {stdout.decode()}")
                print(f"STDERR: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi khởi động GUI server: {e}")
            return False
            
    def start_bot(self):
        """Khởi động bot tiếng Việt"""
        print("🤖 Đang khởi động StudyLion bot (tiếng Việt)...")
        try:
            python_exe = sys.executable
            env = os.environ.copy()
            env['STUDYLION_PRIVATE'] = '1'
            env['STUDYLION_SINGLE_SERVER'] = '1434581250798125068'
            env['LANG'] = 'vi_VN.UTF-8'
            env['LC_ALL'] = 'vi_VN.UTF-8'
            
            self.bot_process = subprocess.Popen([
                python_exe, "scripts/start_leo_vi.py"
            ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            print("✅ Bot đã khởi động thành công")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khởi động bot: {e}")
            return False
            
    def monitor_processes(self):
        """Theo dõi các processes"""
        while self.running:
            try:
                # Kiểm tra GUI server
                if self.gui_process and self.gui_process.poll() is not None:
                    print("⚠️ GUI server đã dừng, đang khởi động lại...")
                    if not self.start_gui_server():
                        print("❌ Không thể khởi động lại GUI server")
                        break
                        
                # Kiểm tra bot
                if self.bot_process and self.bot_process.poll() is not None:
                    print("⚠️ Bot đã dừng, đang khởi động lại...")
                    if not self.start_bot():
                        print("❌ Không thể khởi động lại bot")
                        break
                        
                # Hiển thị output của bot
                if self.bot_process:
                    try:
                        line = self.bot_process.stdout.readline()
                        if line:
                            print(line.decode().strip())
                    except:
                        pass
                        
                time.sleep(1)
                
            except KeyboardInterrupt:
                break
                
    def run(self):
        """Chạy bot manager"""
        # Thiết lập signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 Khởi động StudyLion Bot Tiếng Việt với GUI")
        print("=" * 50)
        
        # Khởi động GUI server trước
        if not self.start_gui_server():
            print("❌ Không thể khởi động mà không có GUI server")
            return 1
            
        # Khởi động bot
        if not self.start_bot():
            print("❌ Không thể khởi động bot")
            self.cleanup()
            return 1
            
        print("🎉 Tất cả dịch vụ đã khởi động thành công!")
        print("📊 Render ảnh leaderboard đã sẵn sàng")
        print("🇻🇳 Bot sử dụng tiếng Việt")
        print("Nhấn Ctrl+C để dừng")
        print("=" * 50)
        
        # Theo dõi processes
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
            
        return 0

def main():
    manager = VietnameseBotManager()
    return manager.run()

if __name__ == '__main__':
    sys.exit(main())