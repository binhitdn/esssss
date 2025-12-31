#!/usr/bin/env python3
"""
Discord Role Analyzer
Script phân tích tất cả roles trong server Discord
"""
import discord
import asyncio
import os
import json
from datetime import datetime
import pytz

# Đọc token từ config
def get_bot_token():
    try:
        with open('config/secrets.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('token =') or line.startswith('TOKEN ='):
                    return line.split('=')[1].strip()
    except:
        print("❌ Không thể đọc token từ config/secrets.conf")
        return None
    return None

# Server ID
GUILD_ID = 1434581250798125068

class RoleAnalyzer(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        
    async def on_ready(self):
        print(f"🤖 Bot connected: {self.user}")
        
        guild = self.get_guild(GUILD_ID)
        if not guild:
            print(f"❌ Không tìm thấy server với ID: {GUILD_ID}")
            await self.close()
            return
        
        print(f"📊 Analyzing server: {guild.name}")
        print(f"👥 Total members: {guild.member_count}")
        print("=" * 60)
        
        # Phân tích roles
        await self.analyze_roles(guild)
        
        # Tạo file JSON cho web
        await self.export_role_data(guild)
        
        await self.close()
    
    async def analyze_roles(self, guild):
        """Phân tích tất cả roles trong server"""
        roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
        
        print("🔍 PHÂN TÍCH ROLES:")
        print("=" * 60)
        
        admin_roles = []
        top_week_roles = []
        special_roles = []
        normal_roles = []
        
        for role in roles:
            if role.name == "@everyone":
                continue
                
            member_count = len(role.members)
            
            # Phân loại roles
            role_name_lower = role.name.lower()
            
            if any(keyword in role_name_lower for keyword in ["super admin", "admin", "group manager"]):
                admin_roles.append(role)
                category = "👑 ADMIN"
            elif "top" in role_name_lower and "week" in role_name_lower:
                top_week_roles.append(role)
                category = "🏆 TOP WEEK"
            elif any(keyword in role_name_lower for keyword in ["mod", "staff", "vip", "premium", "special"]):
                special_roles.append(role)
                category = "⭐ SPECIAL"
            else:
                normal_roles.append(role)
                category = "👤 NORMAL"
            
            # In thông tin role
            color_hex = str(role.color) if role.color != discord.Color.default() else "#99AAB5"
            permissions = role.permissions
            
            print(f"{category} | {role.name}")
            print(f"   👥 Members: {member_count}")
            print(f"   🎨 Color: {color_hex}")
            print(f"   📍 Position: {role.position}")
            print(f"   🔒 Permissions: {self.get_key_permissions(permissions)}")
            
            if member_count > 0 and member_count <= 10:
                member_names = [m.display_name for m in role.members[:10]]
                print(f"   📋 Members: {', '.join(member_names)}")
            
            print()
        
        # Tổng kết
        print("📊 TỔNG KẾT:")
        print("=" * 60)
        print(f"👑 Admin roles: {len(admin_roles)}")
        print(f"🏆 Top Week roles: {len(top_week_roles)}")
        print(f"⭐ Special roles: {len(special_roles)}")
        print(f"👤 Normal roles: {len(normal_roles)}")
        print(f"📊 Total roles: {len(roles) - 1}")  # -1 để loại bỏ @everyone
        
        return {
            'admin_roles': admin_roles,
            'top_week_roles': top_week_roles,
            'special_roles': special_roles,
            'normal_roles': normal_roles
        }
    
    def get_key_permissions(self, permissions):
        """Lấy các quyền quan trọng"""
        key_perms = []
        
        if permissions.administrator:
            key_perms.append("Administrator")
        if permissions.manage_guild:
            key_perms.append("Manage Server")
        if permissions.manage_roles:
            key_perms.append("Manage Roles")
        if permissions.manage_channels:
            key_perms.append("Manage Channels")
        if permissions.kick_members:
            key_perms.append("Kick Members")
        if permissions.ban_members:
            key_perms.append("Ban Members")
        if permissions.manage_messages:
            key_perms.append("Manage Messages")
        
        return ", ".join(key_perms) if key_perms else "Basic"
    
    async def export_role_data(self, guild):
        """Xuất dữ liệu roles ra file JSON"""
        roles_data = []
        
        for role in guild.roles:
            if role.name == "@everyone":
                continue
                
            role_data = {
                'id': str(role.id),
                'name': role.name,
                'color': str(role.color),
                'position': role.position,
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
                'members': [
                    {
                        'id': str(member.id),
                        'name': member.display_name,
                        'username': str(member),
                        'avatar': str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
                        'joined_at': member.joined_at.isoformat() if member.joined_at else None,
                        'status': str(member.status)
                    }
                    for member in role.members[:50]  # Giới hạn 50 members đầu tiên
                ],
                'category': self.categorize_role(role.name)
            }
            
            roles_data.append(role_data)
        
        # Sắp xếp theo position
        roles_data.sort(key=lambda r: r['position'], reverse=True)
        
        # Xuất ra file
        output_data = {
            'server': {
                'id': str(guild.id),
                'name': guild.name,
                'member_count': guild.member_count,
                'created_at': guild.created_at.isoformat(),
                'owner': guild.owner.display_name if guild.owner else None,
                'icon_url': str(guild.icon.url) if guild.icon else None
            },
            'roles': roles_data,
            'analyzed_at': datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).isoformat(),
            'statistics': {
                'total_roles': len(roles_data),
                'admin_roles': len([r for r in roles_data if r['category'] == 'admin']),
                'top_week_roles': len([r for r in roles_data if r['category'] == 'top_week']),
                'special_roles': len([r for r in roles_data if r['category'] == 'special']),
                'normal_roles': len([r for r in roles_data if r['category'] == 'normal'])
            }
        }
        
        # Tạo thư mục web/data nếu chưa có
        os.makedirs('web/data', exist_ok=True)
        
        with open('web/data/roles_data.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print("💾 Đã xuất dữ liệu ra web/data/roles_data.json")
        print("🌐 Có thể sử dụng cho web dashboard")
    
    def categorize_role(self, role_name):
        """Phân loại role"""
        role_name_lower = role_name.lower()
        
        if any(keyword in role_name_lower for keyword in ["super admin", "admin", "group manager"]):
            return "admin"
        elif "top" in role_name_lower and "week" in role_name_lower:
            return "top_week"
        elif any(keyword in role_name_lower for keyword in ["mod", "staff", "vip", "premium", "special"]):
            return "special"
        else:
            return "normal"

async def main():
    """Main function"""
    print("🔍 Discord Role Analyzer")
    print("=" * 40)
    
    token = get_bot_token()
    if not token:
        print("❌ Không có token Discord!")
        return 1
    
    client = RoleAnalyzer()
    
    try:
        await client.start(token)
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(asyncio.run(main()))