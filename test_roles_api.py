#!/usr/bin/env python3
"""
Test Roles API
Script test API roles mới
"""
import requests
import json
import time

def test_roles_api():
    """Test API roles"""
    try:
        print("🧪 Testing Roles API...")
        
        # Đợi server khởi động
        time.sleep(3)
        
        response = requests.get('http://localhost:5001/api/stats', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Response OK")
            
            # In thông tin server
            if 'stats' in data and 'server' in data['stats']:
                server = data['stats']['server']
                print(f"📊 Server: {server.get('name', 'N/A')}")
                print(f"👥 Members: {server.get('member_count', 'N/A')}")
                print(f"🟢 Online: {server.get('online_count', 'N/A')}")
            
            # In thông tin roles
            if 'stats' in data and 'roles' in data['stats']:
                roles = data['stats']['roles']
                print(f"\n🏷️ ROLES STATISTICS:")
                print(f"   👑 Admin roles: {len(roles.get('admin_roles', []))}")
                print(f"   🏆 Top Week roles: {len(roles.get('top_week_roles', []))}")
                print(f"   ⭐ Special roles: {len(roles.get('special_roles', []))}")
                print(f"   📊 Total roles: {roles.get('statistics', {}).get('total_count', 'N/A')}")
                
                # In chi tiết admin roles
                admin_roles = roles.get('admin_roles', [])
                if admin_roles:
                    print(f"\n👑 ADMIN ROLES:")
                    for role in admin_roles:
                        print(f"   - {role['name']}: {role['member_count']} members")
                
                # In chi tiết top week roles
                top_week_roles = roles.get('top_week_roles', [])
                if top_week_roles:
                    print(f"\n🏆 TOP WEEK ROLES:")
                    for role in top_week_roles:
                        print(f"   - {role['name']}: {role['member_count']} members")
            
            return True
        else:
            print(f"❌ API Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = test_roles_api()
    if success:
        print("\n🎉 Test passed! Web dashboard is working.")
        print("🌐 Access: http://localhost:5001")
    else:
        print("\n❌ Test failed!")
    
    exit(0 if success else 1)