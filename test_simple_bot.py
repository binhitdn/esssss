#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio

# Đọc token
with open('config/secrets.conf', 'r') as f:
    for line in f:
        if 'token' in line.lower():
            token = line.split('=')[1].strip()
            break

print("Creating bot...")
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")
    print("Bot đang chạy... Nhấn Ctrl+C để tắt")

print("Starting bot...")
try:
    bot.run(token)
except KeyboardInterrupt:
    print("\n🛑 Đang tắt bot...")
except Exception as e:
    print(f"❌ Lỗi: {e}")
    import traceback
    traceback.print_exc()
