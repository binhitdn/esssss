#!/usr/bin/env python3
"""Test bot startup"""
import sys
import traceback

try:
    print("Importing modules...")
    import discord
    from discord.ext import commands
    print("✅ Discord imported")
    
    import asyncio
    print("✅ Asyncio imported")
    
    # Test reading token
    print("Reading token...")
    with open('config/secrets.conf', 'r') as f:
        for line in f:
            if 'token' in line.lower():
                token = line.split('=')[1].strip()
                print(f"✅ Token found: {token[:20]}...")
                break
    
    # Test bot creation
    print("Creating bot...")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    bot = commands.Bot(
        command_prefix='/',
        intents=intents,
        help_command=None
    )
    print("✅ Bot created")
    
    @bot.event
    async def on_ready():
        print(f"✅ Bot online: {bot.user}")
        await bot.close()
    
    print("Starting bot...")
    asyncio.run(bot.start(token))
    print("✅ Bot started successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
