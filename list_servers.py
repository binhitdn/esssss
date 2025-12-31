#!/usr/bin/env python3
"""
List Discord Servers
Script để xem tất cả servers mà bot có thể truy cập
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

class ServerLister(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(intents=intents)
        
    async def on_ready(self):
        print(f"🤖 Connected: {self.user}")
        print("=" * 60)
        
        if not self.guilds:
            print("❌ Bot không có trong server nào!")
            print("💡 Hãy invite bot vào server trước")
        else:
            print(f"📊 Bot có trong {len(self.guilds)} server(s):")
            print()
            
            for i, guild in enumerate(self.guilds, 1):
                print(f"{i}. {guild.name}")
                print(f"   ID: {guild.id}")
                print(f"   Members: {guild.member_count}")
                print(f"   Owner: {guild.owner}")
                print(f"   Created: {guild.created_at.strftime('%Y-%m-%d')}")
                
                # Kiểm tra permissions
                me = guild.me
                if me:
                    perms = me.guild_permissions
                    important_perms = []
                    if perms.administrator:
                        important_perms.append("Administrator")
                    if perms.manage_guild:
                        important_perms.append("Manage Server")
                    if perms.manage_roles:
                        important_perms.append("Manage Roles")
                    if perms.view_audit_log:
                        important_perms.append("View Audit Log")
                    
                    if important_perms:
                        print(f"   Permissions: {', '.join(important_perms)}")
                    else:
                        print(f"   Permissions: Basic")
                
                print()
        
        await self.close()

async def main():
    token = get_token()
    if not token:
        print("❌ No token found!")
        print("Add your token to config/roles_token.conf:")
        print("token = YOUR_TOKEN_HERE")
        return 1
    
    client = ServerLister()
    await client.start(token)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(asyncio.run(main()))