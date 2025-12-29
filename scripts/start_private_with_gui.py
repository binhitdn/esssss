#!/usr/bin/env python3
"""
Complete startup script for private StudyLion bot with GUI rendering support.
Starts both GUI server and bot for full functionality including leaderboards.
"""
import sys
import os
import asyncio
import subprocess
import time
import signal
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class BotManager:
    def __init__(self):
        self.gui_process = None
        self.bot_process = None
        self.running = True
        
    def signal_handler(self, signum, frame):
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        
    def cleanup(self):
        """Clean shutdown of all processes"""
        if self.gui_process:
            print("🔄 Stopping GUI server...")
            self.gui_process.terminate()
            try:
                self.gui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.gui_process.kill()
                
        if self.bot_process:
            print("🔄 Stopping bot...")
            self.bot_process.terminate()
            try:
                self.bot_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.bot_process.kill()
                
        # Clean up socket file
        socket_path = Path("gui.sock")
        if socket_path.exists():
            socket_path.unlink()
            
        print("✅ Cleanup complete")
        
    def start_gui_server(self):
        """Start GUI rendering server"""
        print("🎨 Starting GUI server...")
        try:
            # Use the same Python executable that's running this script
            python_exe = sys.executable
            # Set environment to match current process
            env = os.environ.copy()
            self.gui_process = subprocess.Popen([
                python_exe, "scripts/start_gui.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            
            # Wait a bit for GUI server to start
            time.sleep(3)
            
            if self.gui_process.poll() is None:
                print("✅ GUI server started successfully")
                return True
            else:
                stdout, stderr = self.gui_process.communicate()
                print(f"❌ GUI server failed to start:")
                print(f"STDOUT: {stdout.decode()}")
                print(f"STDERR: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start GUI server: {e}")
            return False
            
    def start_bot(self):
        """Start the bot"""
        print("🤖 Starting StudyLion bot...")
        try:
            # Set environment variables for private bot
            env = os.environ.copy()
            env['STUDYLION_PRIVATE'] = '1'
            env['STUDYLION_SINGLE_SERVER'] = '1434581250798125068'  # Server: "14 hours a days"
            env['STUDYLION_LOCALE'] = 'vi'  # Tiếng Việt / Vietnamese language

            
            # Use the same Python executable that's running this script
            python_exe = sys.executable
            self.bot_process = subprocess.Popen([
                python_exe, "scripts/start_leo.py"
            ], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            print("✅ Bot started successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
            return False
            
    def monitor_processes(self):
        """Monitor both processes and restart if needed"""
        while self.running:
            try:
                # Check GUI server
                if self.gui_process and self.gui_process.poll() is not None:
                    print("⚠️ GUI server stopped, restarting...")
                    if not self.start_gui_server():
                        print("❌ Failed to restart GUI server")
                        break
                        
                # Check bot
                if self.bot_process and self.bot_process.poll() is not None:
                    print("⚠️ Bot stopped, restarting...")
                    if not self.start_bot():
                        print("❌ Failed to restart bot")
                        break
                        
                # Show bot output
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
        """Main run method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 Starting StudyLion Private Bot with GUI Support")
        print("=" * 50)
        
        # Start GUI server first
        if not self.start_gui_server():
            print("❌ Cannot start without GUI server")
            return 1
            
        # Start bot
        if not self.start_bot():
            print("❌ Cannot start bot")
            self.cleanup()
            return 1
            
        print("🎉 All services started successfully!")
        print("📊 Leaderboard rendering is now available")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        # Monitor processes
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
            
        return 0

def main():
    manager = BotManager()
    return manager.run()

if __name__ == '__main__':
    sys.exit(main())