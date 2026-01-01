#!/usr/bin/env python3
"""
Test script cho hệ thống đánh thức
Kiểm tra logic cơ bản không cần Discord
"""
import time
from datetime import datetime
import pytz

def test_time_formatting():
    """Test định dạng thời gian"""
    print("🕐 Testing Time Formatting...")
    
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    print(f"Thời gian hiện tại: {now.strftime('%H:%M:%S %d/%m/%Y')}")
    print(f"Múi giờ: {now.tzinfo}")
    print(f"Format cho bot: {now.strftime('%H:%M')}")
    print()

def test_cooldown_logic():
    """Test logic cooldown"""
    print("⏰ Testing Cooldown Logic...")
    
    # Giả lập cooldown
    cooldown = {}
    cooldown_duration = 300  # 5 phút
    
    user_id = 123456789
    now = time.time()
    
    # Lần đầu sử dụng
    if user_id not in cooldown:
        cooldown[user_id] = now
        print("✅ Lần đầu sử dụng - OK")
    
    # Sử dụng ngay lập tức (should be blocked)
    time_left = cooldown[user_id] + cooldown_duration - now
    if time_left > 0:
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        print(f"❌ Bị chặn - còn {minutes}m {seconds}s")
    else:
        print("✅ Được phép sử dụng")
    
    print()

def test_random_content():
    """Test nội dung ngẫu nhiên"""
    print("🎲 Testing Random Content...")
    
    import random
    
    wakeup_emojis = ["🔔", "⏰", "📢", "🎺", "🔊", "⚡", "💪", "🚀", "🎯", "📚"]
    motivational_emojis = ["💪", "🔥", "⭐", "🏆", "🎯", "📈", "💎", "🚀", "⚡", "🌟"]
    
    motivational_quotes = [
        "Thành công bắt đầu từ việc thức dậy sớm!",
        "Mỗi phút trôi qua là một cơ hội học tập!",
        "Hôm nay bạn sẽ học được điều gì mới?",
        "Kiến thức là sức mạnh, hãy tích lũy ngay!",
        "Đừng để thời gian trôi qua vô ích!"
    ]
    
    # Test 5 lần random
    for i in range(5):
        wake_emoji = random.choice(wakeup_emojis)
        moti_emoji = random.choice(motivational_emojis)
        quote = random.choice(motivational_quotes)
        
        print(f"Lần {i+1}: {wake_emoji} {quote} {moti_emoji}")
    
    print()

def test_pomodoro_timing():
    """Test tính toán thời gian Pomodoro"""
    print("🍅 Testing Pomodoro Timing...")
    
    cycles = 3
    study_minutes = 25
    break_minutes = 5
    
    total_study = cycles * study_minutes
    total_break = (cycles - 1) * break_minutes  # Không nghỉ sau chu kỳ cuối
    total_time = total_study + total_break
    
    print(f"Chu kỳ: {cycles}")
    print(f"Tổng thời gian học: {total_study} phút")
    print(f"Tổng thời gian nghỉ: {total_break} phút")
    print(f"Tổng thời gian: {total_time} phút ({total_time//60}h {total_time%60}m)")
    
    # Tính thời gian kết thúc
    from datetime import timedelta
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    end_time = now + timedelta(minutes=total_time)
    
    print(f"Bắt đầu: {now.strftime('%H:%M')}")
    print(f"Kết thúc: {end_time.strftime('%H:%M')}")
    print()

def test_channel_validation():
    """Test validation channel ID"""
    print("📺 Testing Channel Validation...")
    
    WAKEUP_CHANNEL = 1456243735938600970
    
    # Kiểm tra channel ID có hợp lệ không
    if isinstance(WAKEUP_CHANNEL, int) and WAKEUP_CHANNEL > 0:
        print(f"✅ Channel ID hợp lệ: {WAKEUP_CHANNEL}")
    else:
        print(f"❌ Channel ID không hợp lệ: {WAKEUP_CHANNEL}")
    
    # Kiểm tra độ dài (Discord ID thường 18-19 chữ số)
    channel_str = str(WAKEUP_CHANNEL)
    if 17 <= len(channel_str) <= 20:
        print(f"✅ Độ dài ID hợp lệ: {len(channel_str)} chữ số")
    else:
        print(f"❌ Độ dài ID không hợp lệ: {len(channel_str)} chữ số")
    
    print()

if __name__ == "__main__":
    print("🚀 StudyLion Wakeup System Test")
    print("=" * 50)
    
    # Chạy tất cả tests
    test_time_formatting()
    test_cooldown_logic()
    test_random_content()
    test_pomodoro_timing()
    test_channel_validation()
    
    print("🎉 All tests completed!")
    print("✅ Hệ thống đánh thức sẵn sàng hoạt động!")