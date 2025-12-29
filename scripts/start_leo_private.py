#!/usr/bin/env python3
"""
Script khởi động tối ưu cho StudyLion bot riêng tư.
Tắt các dịch vụ và tính năng không cần thiết cho single-server deployment.

Optimized startup script for private StudyLion bot.
Disables unnecessary services and features for single-server deployment.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def _main():
    """Main entry point for private bot."""
    # Cấu hình cho bot riêng tư / Set environment variables for private bot optimization
    os.environ['STUDYLION_PRIVATE'] = '1'
    os.environ['STUDYLION_SINGLE_SERVER'] = '1434581250798125068'  # Server: "14 hours a days"
    os.environ['STUDYLION_LOCALE'] = 'vi'  # Tiếng Việt / Vietnamese language
    
    # Import and run the bot
    from bot import _main as bot_main
    bot_main()

if __name__ == '__main__':
    _main()