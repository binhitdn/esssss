#!/usr/bin/env python3
"""
StudyLion Bot - Chỉ Bảng Xếp Hạng
Chỉ có chức năng bảng xếp hạng với GUI
"""
import discord
from discord.ext import commands
import os
import sys
import asyncio
from io import BytesIO

# Dữ liệu giả cho bảng xếp hạng
FAKE_LEADERBOARD_DATA = [
    {"displayName": "Nguyen Van An", "dayTrackTime": 18600, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Tran Thi Mai", "dayTrackTime": 17240, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Le Hoang Minh", "dayTrackTime": 16530, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Pham Quoc Bao", "dayTrackTime": 15420, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Vo Thanh Dat", "dayTrackTime": 14890, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Doan Thu Ha", "dayTrackTime": 13750, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Bui Tuan Kiet", "dayTrackTime": 12900, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Hoang Ngoc Linh", "dayTrackTime": 12180, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Dang Minh Quan", "dayTrackTime": 11540, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"},
    {"displayName": "Nguyen Phuong Thao", "dayTrackTime": 10860, "avatarURL": "https://m.media-amazon.com/images/S/pv-target-images/16627900db04b76fae3b64266ca161511422059cd24062fb5d900971003a0b70.jpg"}
]

# Server ID được phép
ALLOWED_SERVER_ID = 1434581250798125068

class LeaderboardBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='/',
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        """Thiết lập bot khi khởi động"""
        print("🤖 Bot bảng xếp hạng đang thiết lập...")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Đã sync {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Lỗi sync commands: {e}")
    
    async def on_ready(self):
        """Khi bot sẵn sàng"""
        print(f"🎉 {self.user} đã online!")
        print(f"🏆 Bot bảng xếp hạng sẵn sàng")
        print(f"🎯 Server được phép: {ALLOWED_SERVER_ID}")
        
        # Set status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="bảng xếp hạng 🏆"
            )
        )
    
    async def on_guild_join(self, guild):
        """Khi bot join server mới"""
        if guild.id != ALLOWED_SERVER_ID:
            print(f"⚠️ Bot join server không được phép: {guild.name} ({guild.id})")
            print("🚪 Đang rời server...")
            await guild.leave()
        else:
            print(f"✅ Bot join server được phép: {guild.name}")

def format_time(seconds):
    """Chuyển đổi giây thành định dạng giờ:phút:giây"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}h {minutes}m {secs}s"

async def render_leaderboard_image(data):
    """Render bảng xếp hạng thành ảnh qua GUI client của LionBot"""
    try:
        # Kiểm tra GUI server có sẵn không
        if not os.path.exists('gui.sock'):
            print("⚠️ GUI server chưa sẵn sàng")
            return None
        
        # Chuẩn bị dữ liệu theo format của LeaderboardCard
        entries = []
        for i, member in enumerate(data, 1):
            entries.append((
                i,  # userid (fake)
                i,  # position
                member["dayTrackTime"],  # time in seconds
                member["displayName"],  # name
                (0, None)  # avatar_key (fake, sẽ dùng default)
            ))
        
        # Import GUI client
        sys.path.insert(0, 'src')
        from gui.client import client as gui_client
        
        # Gửi request qua GUI client
        print("📡 Gửi request tới GUI server...")
        image_data = await gui_client.request(
            route='leaderboard_card',
            args=(),
            kwargs={
                'server_name': '14 hours a day(STUDY VIP)',
                'entries': entries,
                'highlight': None,
                'locale': 'vi'
            }
        )
        
        print(f"✅ Render thành công: {len(image_data)} bytes")
        return image_data
                    
    except Exception as e:
        print(f"❌ Lỗi render ảnh: {e}")
        import traceback
        traceback.print_exc()
        return None

# Tạo bot instance
bot = LeaderboardBot()

@bot.tree.command(name="bangxephang", description="Xem bảng xếp hạng học tập hôm nay")
async def leaderboard_command(interaction: discord.Interaction):
    """Lệnh bảng xếp hạng - Chức năng duy nhất của bot"""
    # Respond ngay lập tức để tránh timeout
    await interaction.response.send_message("🎨 Đang tạo bảng xếp hạng...", ephemeral=True)
    
    try:
        # Render ảnh bảng xếp hạng
        print("🎨 Đang render bảng xếp hạng...")
        image_data = await render_leaderboard_image(FAKE_LEADERBOARD_DATA)
        
        if image_data:
            print(f"📊 Đã nhận image data: {len(image_data)} bytes")
            
            # Gửi ảnh dạng tin nhắn thường (không embed)
            file = discord.File(
                fp=BytesIO(image_data),
                filename="leaderboard.png"
            )
            
            # Gửi tin nhắn mới thay vì followup
            await interaction.channel.send(
                content="🏆 **Bảng Xếp Hạng Học Tập** - Top 10 người học chăm chỉ nhất hôm nay!",
                file=file
            )
            print("✅ Đã gửi bảng xếp hạng với ảnh")
            
        else:
            print("⚠️ Không có image data, gửi fallback text")
            # Fallback: gửi text nếu không render được ảnh
            leaderboard_text = "🏆 **Bảng Xếp Hạng Học Tập**\n\n"
            for i, member in enumerate(FAKE_LEADERBOARD_DATA, 1):
                time_str = format_time(member["dayTrackTime"])
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                leaderboard_text += f"{medal} **{member['displayName']}** - {time_str}\n"
            
            await interaction.channel.send(leaderboard_text)
            print("✅ Đã gửi bảng xếp hạng dạng text")
            
    except Exception as e:
        print(f"❌ Lỗi lệnh bảng xếp hạng: {e}")
        import traceback
        traceback.print_exc()
        
        # Gửi thông báo lỗi
        try:
            await interaction.channel.send("❌ Có lỗi xảy ra khi tạo bảng xếp hạng! Vui lòng thử lại sau.")
        except:
            print("❌ Không thể gửi thông báo lỗi")

async def main():
    """Hàm main để chạy bot"""
    # Đọc token từ config
    token = None
    try:
        with open('config/secrets.conf', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('token =') or line.startswith('TOKEN ='):
                    token = line.split('=')[1].strip()
                    break
    except:
        print("❌ Không thể đọc token từ config/secrets.conf")
        return
    
    if not token:
        print("❌ Không tìm thấy token trong config")
        return
    
    print("🚀 Khởi động Bot Bảng Xếp Hạng")
    print("=" * 40)
    print("🎯 Server: ", ALLOWED_SERVER_ID)
    print("🏆 Chức năng: Chỉ bảng xếp hạng")
    print("🎨 GUI: Có hỗ trợ render ảnh")
    print("=" * 40)
    
    try:
        await bot.start(token)
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")

if __name__ == '__main__':
    asyncio.run(main())