#!/usr/bin/env python3
"""
Test các lệnh tiếng Việt của bot
"""
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_translations():
    """Test xem các dịch có hoạt động không"""
    print("🧪 Kiểm tra hệ thống dịch tiếng Việt...")
    
    try:
        # Import babel system
        from babel.translator import LeoBabel
        
        # Create translator
        translator = LeoBabel()
        
        # Test some translations
        test_cases = [
            ("cmd:help", "help", "trogiup"),
            ("cmd:me", "me", "toi"), 
            ("cmd:leaderboard", "leaderboard", "bangxephang"),
            ("cmd:timer", "timer", "dongho")
        ]
        
        print("📝 Kiểm tra các dịch:")
        all_passed = True
        
        for context, original, expected in test_cases:
            try:
                # Test translation
                translated = translator.get(original, context=context, locale='vi')
                
                if translated == expected:
                    print(f"   ✅ {original} -> {translated}")
                else:
                    print(f"   ❌ {original} -> {translated} (mong đợi: {expected})")
                    all_passed = False
                    
            except Exception as e:
                print(f"   ❌ Lỗi dịch {original}: {e}")
                all_passed = False
        
        if all_passed:
            print("🎉 Tất cả dịch đều hoạt động!")
        else:
            print("⚠️ Một số dịch có vấn đề")
            
        return all_passed
        
    except Exception as e:
        print(f"❌ Lỗi hệ thống dịch: {e}")
        return False

def check_mo_files():
    """Kiểm tra các file .mo đã được tạo chưa"""
    print("\n📁 Kiểm tra file .mo:")
    
    required_files = [
        "locales/vi/LC_MESSAGES/base.mo",
        "locales/vi/LC_MESSAGES/meta.mo", 
        "locales/vi/LC_MESSAGES/statistics.mo",
        "locales/vi/LC_MESSAGES/Pomodoro.mo"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path} - không tồn tại")
            all_exist = False
    
    return all_exist

async def main():
    """Main test function"""
    print("🚀 Test Hệ Thống Tiếng Việt StudyLion")
    print("=" * 45)
    
    # Test 1: Check .mo files
    mo_ok = check_mo_files()
    
    # Test 2: Test translations
    trans_ok = await test_translations()
    
    print("\n" + "=" * 45)
    print("📋 KẾT QUẢ:")
    print(f"   File .mo: {'✅ OK' if mo_ok else '❌ FAIL'}")
    print(f"   Dịch thuật: {'✅ OK' if trans_ok else '❌ FAIL'}")
    
    if mo_ok and trans_ok:
        print("\n🎉 HỆ THỐNG TIẾNG VIỆT HOẠT ĐỘNG!")
        print("🇻🇳 Bot sẽ hiển thị lệnh bằng tiếng Việt")
        print("\n📋 Các lệnh có sẵn:")
        print("   /trogiup - Trợ giúp")
        print("   /toi - Profile cá nhân") 
        print("   /bangxephang - Bảng xếp hạng")
        print("   /dongho - Timer pomodoro")
    else:
        print("\n⚠️ CÓ VẤN ĐỀ VỚI HỆ THỐNG TIẾNG VIỆT")
        print("Bot có thể vẫn hiển thị tiếng Anh")

if __name__ == '__main__':
    asyncio.run(main())