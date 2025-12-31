#!/usr/bin/env python3
"""
Test Web API
Script test các API endpoint của web dashboard
"""
import requests
import json
import time

def test_api_endpoint(url, name):
    """Test một API endpoint"""
    try:
        print(f"🧪 Testing {name}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name}: OK")
            
            # In một số thông tin cơ bản
            if 'stats' in data:
                if 'server' in data['stats']:
                    server = data['stats']['server']
                    print(f"   📊 Server: {server.get('name', 'N/A')}")
                    print(f"   👥 Members: {server.get('member_count', 'N/A')}")
                    print(f"   🟢 Online: {server.get('online_count', 'N/A')}")
                
                if 'members' in data['stats']:
                    members = data['stats']['members']
                    print(f"   👤 Total: {members.get('total', 'N/A')}")
                    print(f"   🤖 Bots: {members.get('bots', 'N/A')}")
            
            if 'data' in data:
                print(f"   📋 Data items: {len(data['data'])}")
                
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Testing StudyLion Web API")
    print("=" * 40)
    
    base_url = "http://localhost:5001"
    
    # Test các endpoint
    endpoints = [
        (f"{base_url}/api/stats", "Server Stats"),
        (f"{base_url}/api/server", "Server Data"),
        (f"{base_url}/api/leaderboard/day", "Leaderboard Day"),
        (f"{base_url}/api/leaderboard/week", "Leaderboard Week"),
        (f"{base_url}/api/leaderboard/month", "Leaderboard Month"),
    ]
    
    results = []
    for url, name in endpoints:
        result = test_api_endpoint(url, name)
        results.append((name, result))
        print()
        time.sleep(1)  # Đợi 1 giây giữa các request
    
    # Tổng kết
    print("📊 Test Results:")
    print("=" * 40)
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Summary: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Web dashboard is working correctly.")
        print("\n🌐 Access the dashboard at:")
        print(f"   Main Dashboard: {base_url}/")
        print(f"   Leaderboard: {base_url}/leaderboard")
        print(f"   Advanced Analytics: {base_url}/advanced")
    else:
        print("⚠️ Some tests failed. Check the web server logs.")
    
    return 0 if passed == len(results) else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())