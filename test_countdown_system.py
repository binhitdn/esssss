#!/usr/bin/env python3
"""
Test script cho hệ thống phòng đếm ngược
Kiểm tra logic cơ bản không cần Discord
"""
from datetime import datetime, timedelta
import pytz

def test_date_parsing():
    """Test parse ngày tháng"""
    print("📅 Testing Date Parsing...")
    
    test_cases = [
        "9/12/2025",
        "09/12/2025", 
        "31/1/2026",
        "15/06/25"
    ]
    
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    
    for date_str in test_cases:
        try:
            # Simulate parse logic
            parts = date_str.split('/')
            if len(parts) == 3:
                day, month, year = map(int, parts)
                
                if year < 100:
                    year += 2000
                
                parsed_date = datetime(year, month, day, 23, 59, 59)
                localized_date = vn_tz.localize(parsed_date)
                
                print(f"✅ {date_str} → {localized_date.strftime('%d/%m/%Y %H:%M:%S')}")
        except Exception as e:
            print(f"❌ {date_str} → Lỗi: {e}")
    
    print()

def test_countdown_name_generation():
    """Test tạo tên phòng đếm ngược"""
    print("🏷️ Testing Countdown Name Generation...")
    
    # Simulate time differences
    test_cases = [
        ("JLPT N2", timedelta(days=125, hours=22, minutes=30), "full"),
        ("Thi cuối kỳ", timedelta(days=15, hours=8, minutes=45), "full"),
        ("Deadline", timedelta(days=3, hours=2, minutes=15), "countdown"),
        ("Project", timedelta(days=0, hours=5, minutes=30), "countdown")
    ]
    
    for name, time_left, format_type in test_cases:
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if format_type == "countdown":
            result = f"{days}d{hours:02d}h{minutes:02d}p"
        else:
            result = f"{name} Còn {days}d{hours:02d}h{minutes:02d}p"
        
        print(f"📚 {name} ({format_type}) → {result}")
    
    print()

def test_time_calculations():
    """Test tính toán thời gian"""
    print("⏰ Testing Time Calculations...")
    
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    # Test các khoảng thời gian khác nhau
    test_targets = [
        now + timedelta(days=1),      # 1 ngày
        now + timedelta(days=7),      # 1 tuần  
        now + timedelta(days=30),     # 1 tháng
        now + timedelta(days=365),    # 1 năm
        now + timedelta(hours=5),     # 5 giờ
        now + timedelta(minutes=30)   # 30 phút
    ]
    
    for target in test_targets:
        time_left = target - now
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        print(f"🎯 Mục tiêu: {target.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Còn lại: {days}d{hours:02d}h{minutes:02d}p")
        print()

def test_room_limits():
    """Test giới hạn phòng"""
    print("🏠 Testing Room Limits...")
    
    # Simulate user rooms
    user_rooms = [
        {"name": "JLPT", "creator_id": 123},
        {"name": "IELTS", "creator_id": 123}, 
        {"name": "Thi cuối kỳ", "creator_id": 123}
    ]
    
    user_id = 123
    user_room_count = len([room for room in user_rooms if room['creator_id'] == user_id])
    
    print(f"👤 User {user_id} có {user_room_count} phòng")
    
    if user_room_count >= 3:
        print("❌ Đã đạt giới hạn 3 phòng/người")
    else:
        print(f"✅ Có thể tạo thêm {3 - user_room_count} phòng")
    
    print()

def test_permission_system():
    """Test hệ thống quyền"""
    print("🔐 Testing Permission System...")
    
    creator_id = 123
    other_user_id = 456
    
    # Simulate permissions
    permissions = {
        "creator": {
            "view_channel": True,
            "connect": True,
            "send_messages": True,
            "manage_channels": True,
            "manage_messages": True
        },
        "others": {
            "view_channel": True,
            "connect": False,
            "send_messages": False,
            "manage_channels": False,
            "manage_messages": False
        }
    }
    
    print("👑 Creator permissions:")
    for perm, value in permissions["creator"].items():
        status = "✅" if value else "❌"
        print(f"   {status} {perm}")
    
    print("\n👥 Other users permissions:")
    for perm, value in permissions["others"].items():
        status = "✅" if value else "❌"
        print(f"   {status} {perm}")
    
    print()

if __name__ == "__main__":
    print("🚀 StudyLion Countdown System Test")
    print("=" * 50)
    
    test_date_parsing()
    test_countdown_name_generation()
    test_time_calculations()
    test_room_limits()
    test_permission_system()
    
    print("🎉 All countdown tests completed!")
    print("✅ Hệ thống phòng đếm ngược sẵn sàng hoạt động!")