#!/usr/bin/env python3
"""
Discord Roles Reader
Script đọc tất cả roles từ Discord server và lưu vào mảng
"""
import discord
import asyncio
import json
import os
from datetime import datetime
import pytz

# Đọc token từ config riêng
def get_discord_token():
    try:
        with open('config/roles_token.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('token ='):
                    token = line.split('=')[1].strip()
                    if token:
                        return token
                    else:
                        print("❌ Token trống! Hãy thêm token vào config/roles_token.conf")
                        return None
    except FileNotFoundError:
        print("❌ Không tìm thấy file config/roles_token.conf")
        return None
    except Exception as e:
        print(f"❌ Lỗi đọc token: {e}")
        return None
    
    print("❌ Không tìm thấy token trong config/roles_token.conf")
    return None

def get_guild_id():
    try:
        with open('config/roles_token.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('guild_id ='):
                    return int(line.split('=')[1].strip())
    except:
        pass
    return 1434581250798125068  # Default

class RolesReader(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        
        self.guild_id = get_guild_id()
        self.roles_data = []
        
    async def on_ready(self):
        print(f"🤖 Bot connected: {self.user}")
        
        guild = self.get_guild(self.guild_id)
        if not guild:
            print(f"❌ Không tìm thấy server với ID: {self.guild_id}")
            await self.close()
            return
        
        print(f"📊 Reading roles from server: {guild.name}")
        print(f"👥 Total members: {guild.member_count}")
        print("=" * 60)
        
        # Đọc tất cả roles
        await self.read_all_roles(guild)
        
        # Xuất dữ liệu
        await self.export_roles_data(guild)
        
        await self.close()
    
    async def read_all_roles(self, guild):
        """Đọc tất cả roles và lưu vào mảng"""
        print("🔍 ĐANG ĐỌC TẤT CẢ ROLES:")
        print("=" * 60)
        
        roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        
        for i, role in enumerate(roles):
            if role.name == "@everyone":
                continue
                
            role_info = {
                'id': str(role.id),
                'name': role.name,
                'position': role.position,
                'color': str(role.color),
                'member_count': len(role.members),
                'permissions': {
                    'administrator': role.permissions.administrator,
                    'manage_guild': role.permissions.manage_guild,
                    'manage_roles': role.permissions.manage_roles,
                    'manage_channels': role.permissions.manage_channels,
                    'kick_members': role.permissions.kick_members,
                    'ban_members': role.permissions.ban_members,
                    'manage_messages': role.permissions.manage_messages
                },
                'mentionable': role.mentionable,
                'hoist': role.hoist,
                'created_at': role.created_at.isoformat() if role.created_at else None
            }
            
            self.roles_data.append(role_info)
            
            # In thông tin role
            print(f"{i+1:3d}. {role.name}")
            print(f"     ID: {role.id}")
            print(f"     Members: {len(role.members)}")
            print(f"     Color: {role.color}")
            print(f"     Position: {role.position}")
            
            # In permissions quan trọng
            perms = []
            if role.permissions.administrator:
                perms.append("Administrator")
            if role.permissions.manage_guild:
                perms.append("Manage Server")
            if role.permissions.manage_roles:
                perms.append("Manage Roles")
            if role.permissions.kick_members:
                perms.append("Kick Members")
            if role.permissions.ban_members:
                perms.append("Ban Members")
            
            if perms:
                print(f"     Permissions: {', '.join(perms)}")
            
            print()
        
        print(f"✅ Đã đọc {len(self.roles_data)} roles")
    
    async def export_roles_data(self, guild):
        """Xuất dữ liệu roles ra các file khác nhau"""
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vn_tz)
        
        # Tạo thư mục output nếu chưa có
        os.makedirs('output', exist_ok=True)
        
        # 1. File JSON đầy đủ
        full_data = {
            'server': {
                'id': str(guild.id),
                'name': guild.name,
                'member_count': guild.member_count,
                'created_at': guild.created_at.isoformat(),
                'owner': guild.owner.display_name if guild.owner else None
            },
            'roles': self.roles_data,
            'total_roles': len(self.roles_data),
            'exported_at': now.isoformat(),
            'exported_by': str(self.user)
        }
        
        with open('output/all_roles_full.json', 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        
        print("💾 Đã xuất dữ liệu đầy đủ ra output/all_roles_full.json")
        
        # 2. File JSON đơn giản (chỉ ID và tên)
        simple_roles = [
            {
                'id': role['id'],
                'name': role['name']
            }
            for role in self.roles_data
        ]
        
        simple_data = {
            'server_id': str(guild.id),
            'server_name': guild.name,
            'roles': simple_roles,
            'total': len(simple_roles),
            'exported_at': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('output/roles_simple.json', 'w', encoding='utf-8') as f:
            json.dump(simple_data, f, ensure_ascii=False, indent=2)
        
        print("💾 Đã xuất dữ liệu đơn giản ra output/roles_simple.json")
        
        # 3. File Python array
        python_array = "# Discord Roles Array\n"
        python_array += f"# Server: {guild.name} ({guild.id})\n"
        python_array += f"# Exported: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        python_array += "DISCORD_ROLES = [\n"
        
        for role in self.roles_data:
            python_array += f"    {{'id': '{role['id']}', 'name': '{role['name']}'}},\n"
        
        python_array += "]\n\n"
        python_array += f"# Total roles: {len(self.roles_data)}\n"
        
        with open('output/roles_array.py', 'w', encoding='utf-8') as f:
            f.write(python_array)
        
        print("💾 Đã xuất Python array ra output/roles_array.py")
        
        # 4. File CSV
        csv_content = "ID,Name,Position,MemberCount,Color,Administrator,ManageGuild\n"
        for role in self.roles_data:
            csv_content += f"{role['id']},{role['name']},{role['position']},{role['member_count']},{role['color']},{role['permissions']['administrator']},{role['permissions']['manage_guild']}\n"
        
        with open('output/roles.csv', 'w', encoding='utf-8') as f:
            f.write(csv_content)
        
        print("💾 Đã xuất CSV ra output/roles.csv")
        
        # 5. In mảng JavaScript
        js_array = "// Discord Roles Array\n"
        js_array += f"// Server: {guild.name} ({guild.id})\n"
        js_array += f"// Exported: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        js_array += "const DISCORD_ROLES = [\n"
        
        for role in self.roles_data:
            js_array += f"    {{id: '{role['id']}', name: '{role['name']}'}},\n"
        
        js_array += "];\n\n"
        js_array += f"// Total roles: {len(self.roles_data)}\n"
        
        with open('output/roles_array.js', 'w', encoding='utf-8') as f:
            f.write(js_array)
        
        print("💾 Đã xuất JavaScript array ra output/roles_array.js")
        
        # In tổng kết
        print("\n📊 TỔNG KẾT:")
        print("=" * 60)
        print(f"📁 Server: {guild.name}")
        print(f"🆔 Server ID: {guild.id}")
        print(f"🏷️ Total roles: {len(self.roles_data)}")
        print(f"📅 Exported at: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📂 Files created:")
        print("   - output/all_roles_full.json (đầy đủ)")
        print("   - output/roles_simple.json (đơn giản)")
        print("   - output/roles_array.py (Python array)")
        print("   - output/roles_array.js (JavaScript array)")
        print("   - output/roles.csv (CSV)")

async def main():
    """Main function"""
    print("🔍 Discord Roles Reader")
    print("=" * 40)
    
    token = get_discord_token()
    if not token:
        print("\n💡 Hướng dẫn:")
        print("1. Mở file config/roles_token.conf")
        print("2. Thêm token Discord vào dòng: token = YOUR_TOKEN_HERE")
        print("3. Chạy lại script này")
        return 1
    
    print(f"✅ Đã đọc token: {token[:20]}...")
    
    client = RolesReader()
    
    try:
        await client.start(token)
    except discord.LoginFailure:
        print("❌ Token không hợp lệ!")
        return 1
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(asyncio.run(main()))