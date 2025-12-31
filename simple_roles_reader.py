#!/usr/bin/env python3
"""
Simple Discord Roles Reader
Script đơn giản để lấy ID và tên tất cả roles
"""
import discord
import asyncio
import json

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

# Server ID
GUILD_ID = 1434581250798125068

class SimpleRolesReader(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        super().__init__(intents=intents)
        
    async def on_ready(self):
        print(f"🤖 Connected: {self.user}")
        
        guild = self.get_guild(GUILD_ID)
        if not guild:
            print(f"❌ Server not found: {GUILD_ID}")
            await self.close()
            return
        
        print(f"📊 Server: {guild.name}")
        print("=" * 50)
        
        # Lấy tất cả roles
        roles_array = []
        
        for role in sorted(guild.roles, key=lambda r: r.position, reverse=True):
            if role.name == "@everyone":
                continue
                
            roles_array.append({
                'id': str(role.id),
                'name': role.name
            })
            
            print(f"ID: {role.id} | Name: {role.name}")
        
        print("=" * 50)
        print(f"Total roles: {len(roles_array)}")
        
        # Lưu vào file JSON
        with open('roles_list.json', 'w', encoding='utf-8') as f:
            json.dump(roles_array, f, ensure_ascii=False, indent=2)
        
        print("💾 Saved to roles_list.json")
        
        # In Python array
        print("\n🐍 PYTHON ARRAY:")
        print("roles = [")
        for role in roles_array:
            print(f"    {{'id': '{role['id']}', 'name': '{role['name']}'}},")
        print("]")
        
        await self.close()

async def main():
    token = get_token()
    if not token:
        print("❌ No token found!")
        print("Add your token to config/roles_token.conf:")
        print("token = YOUR_TOKEN_HERE")
        return 1
    
    client = SimpleRolesReader()
    await client.start(token)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(asyncio.run(main()))