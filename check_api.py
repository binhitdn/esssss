
import sys
import socket
from urllib.parse import urlparse
import requests

API_URL = "https://api.14study.io.vn/api/leaderboard/top-learners"

print(f"--- Checking Connection to API: {API_URL} ---")

parsed = urlparse(API_URL)
host = parsed.hostname
port = parsed.port or 80

print(f"Host: {host}")
print(f"Port: {port}")

# 1. Check IP type
if host.startswith("192.168.") or host.startswith("10.") or (host.startswith("172.") and 16 <= int(host.split('.')[1]) <= 31):
    print("\n⚠️ WARNING: You are trying to connect to a PRIVATE IP ADDRESS.")
    print(f"This IP ({host}) only works inside your local home/office network.")
    print("A remote Cloud VPS CANNOT reach this IP directly.")
else:
    print("\n✅ IP appears to be public (or invalid).")

# 2. Test Ping (optional, relies on system ping)
import subprocess
print("\n--- Pinging Host ---")
try:
    outcome = subprocess.run(['ping', '-c', '3', host], capture_output=True, text=True, timeout=5)
    if outcome.returncode == 0:
        print("✅ Ping successful")
    else:
        print("❌ Ping failed (Host unreachable)")
except Exception as e:
    print(f"⚠️ Could not help ping: {e}")

# 3. Test TCP Connection
print("\n--- Testing TCP Connection ---")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((host, port))
    if result == 0:
        print("✅ TCP Port is OPEN")
    else:
        print(f"❌ TCP Port is CLOSED or FILTERED (Error: {result})")
    sock.close()
except Exception as e:
    print(f"❌ Socket error: {e}")

# 4. Test HTTP Request
print("\n--- Testing HTTP Request ---")
try:
    response = requests.get(API_URL, timeout=5)
    print(f"Outcome: Status {response.status_code}")
    if response.status_code == 200:
        print("✅ API is responding correctly!")
        print(f"Data sample: {str(response.content)[:100]}...")
    else:
        print("❌ API returned error status")
except Exception as e:
    print(f"❌ HTTP Request failed: {e}")

print("\n------------------------------")
print("CONCLUSION:")
if host.startswith("192.168."):
    print("❌ FAIL: Your VPS cannot connect to 192.168.x.x because it is a private local IP.")
    print("SOLUTION: You need to expose your API to the internet (Public IP/Domain) or use a Tunnel (Cloudflare Tunnel/Ngrok).")
else:
    print("Result depends on above checks.")
