#!/usr/bin/env python3
"""
Generate Bot Invite Link
Script tạo link invite bot vào Discord server
"""
import discord
import asyncio

# Đọc token từ config
def get_token():
    try:
        with open('config/roles_token.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('token ='):
                    token = line.split('=')[1].strip()
                    return token if token else None
    except:
        pass
    return None

class InviteGenerator(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(intents=intents)
        
    async def on_ready(self):
        print(f"🤖 Bot: {self.user}")
        print(f"🆔 Bot ID: {self.user.id}")
        print("=" * 60)
        
        # Tạo invite link với các permissions cần thiết
        permissions = discord.Permissions()
        permissions.read_messages = True
        permissions.view_guild_insights = True
        permissions.manage_roles = True  # Để đọc roles
        permissions.manage_guild = True  # Để đọc server info
        
        invite_url = discord.utils.oauth_url(
            self.user.id,
            permissions=permissions,
            scopes=['bot']
        )
        
        print("🔗 INVITE LINK:")
        print(invite_url)
        print()
        print("📋 Hướng dẫn:")
        print("1. Copy link trên")
        print("2. Mở trong trình duyệt")
        print("3. Chọn server để invite bot")
        print("4. Cấp quyền cho bot")
        print("5. Chạy lại script đọc roles")
        print()
        print("⚠️ Bot cần các quyền:")
        print("   - View Server Insights")
        print("   - Manage Roles")
        print("   - Manage Server")
        
        await self.close()

async def main():
    token = get_token()
    if not token:
        print("❌ No token found!")
        print("Add your token to config/roles_token.conf:")
        print("token = YOUR_TOKEN_HERE")
        return 1
    
    client = InviteGenerator()
    await client.start(token)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(asyncio.run(main()))