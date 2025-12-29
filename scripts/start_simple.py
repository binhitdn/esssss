#!/usr/bin/env python3
"""
Script khởi động đơn giản cho StudyLion Bot đã tối giản hóa.
Chỉ chạy 3 modules chính: Ranks, Statistics, Pomodoro
"""

import sys
import os

# Thêm src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import và chạy bot
from bot import _main

if __name__ == '__main__':
    print("=" * 60)
    print("🦁 StudyLion Bot - Phiên bản tối giản")
    print("=" * 60)
    print("Modules đang chạy:")
    print("  ✓ Bảng xếp hạng (Ranks)")
    print("  ✓ Thống kê học tập (Statistics)")
    print("  ✓ Pomodoro Timer")
    print("=" * 60)
    print()
    
    _main()
