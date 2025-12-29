#!/usr/bin/env python3
"""
Khởi động StudyLion với tiếng Việt đơn giản
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def _main():
    """Main entry point với tiếng Việt"""
    # Set environment cho tiếng Việt
    os.environ['LANG'] = 'vi_VN.UTF-8'
    os.environ['LC_ALL'] = 'vi_VN.UTF-8'
    
    # Import và chạy bot
    from bot import _main as bot_main
    bot_main()

if __name__ == '__main__':
    _main()