#!/usr/bin/env python3
"""
Web Dashboard Configuration
Cấu hình cho web dashboard
"""
import os

# Discord Server Configuration
DISCORD_SERVER_ID = 1434581250798125068  # Thay đổi ID server của bạn ở đây

# Web Server Configuration
WEB_HOST = '0.0.0.0'
WEB_PORT = 5001
DEBUG_MODE = True

# Cache Configuration
CACHE_DURATION = 300  # 5 phút (giây)

# Discord API Configuration
DISCORD_TOKEN_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'secrets.conf')

# Timezone
TIMEZONE = 'Asia/Ho_Chi_Minh'

# Server Display Name (nếu muốn override tên server)
SERVER_DISPLAY_NAME = None  # None = sử dụng tên thật từ Discord