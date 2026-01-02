#!/usr/bin/env python3
"""
Script để sync slash commands cho bot
Chạy script này khi thêm lệnh mới
"""
import os
import sys

def create_sync_flag():
    """Tạo file flag để bot sync commands lần khởi động tiếp theo"""
    try:
        with open('.sync_commands', 'w') as f:
            f.write('sync')
        print("✅ Đã tạo flag sync commands")
        print("🔄 Khởi động lại bot để sync các lệnh mới")
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo flag: {e}")
        return False

def main():
    print("🔄 StudyLion Command Sync Tool")
    print("=" * 40)
    
    if os.path.exists('.sync_commands'):
        print("⚠️ Flag sync đã tồn tại")
        choice = input("Có muốn ghi đè không? (y/N): ").lower()
        if choice != 'y':
            print("❌ Hủy bỏ")
            return
    
    if create_sync_flag():
        print("\n📋 Các lệnh sẽ được sync:")
        print("🏆 Bảng xếp hạng:")
        print("  - /bangxephang")
        print("  - /bangxephang-tuan") 
        print("  - /bangxephang-thang")
        
        print("\n🔔 Đánh thức học tập:")
        print("  - /danh-thuc")
        print("  - /danh-thuc-user")
        print("  - /danh-thuc-kenh")
        print("  - /danh-thuc-hen-gio")
        print("  - /danh-thuc-pomodoro")
        print("  - /danh-thuc-stats")
        
        print("\n📚 Phòng học đếm ngược:")
        print("  - /tao-phong-hoc")
        print("  - /xoa-phong-hoc")
        print("  - /danh-sach-phong-hoc")
        
        print("\n⚠️ Warning System:")
        print("  - /list-warning")
        
        print("\n🔧 Debug & Test:")
        print("  - /debug-tasks")
        print("  - /test-leaderboard")
        
        print("\n🚀 Bước tiếp theo:")
        print("1. Khởi động bot: python3 start.py")
        print("2. Bot sẽ tự động sync commands")
        print("3. Đợi 1-2 phút để Discord cập nhật")
        print("4. Kiểm tra lệnh trong Discord")

if __name__ == "__main__":
    main()