#!/usr/bin/env python3
"""
StudyLion Bot - Chỉ Bảng Xếp Hạng
Chỉ có chức năng bảng xếp hạng với GUI
"""
import discord
from discord.ext import commands, tasks
import os
import sys
import asyncio
import aiohttp
import re
from datetime import datetime, timedelta, time
import pytz
from io import BytesIO

# Force UTF-8 encoding for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# API endpoint
API_BASE_URL = "http://192.168.128.173:3001/api/leaderboard/top-learners"

# Server ID được phép
ALLOWED_SERVER_ID = 1434581250798125068

# Channel IDs cho auto-post
CHANNEL_DAILY = 1450690801934930124      # Bảng xếp hạng ngày - 2h58 mỗi ngày
CHANNEL_WEEKLY = 1435035898629591040     # Bảng xếp hạng tuần - 20h và 2h55 mỗi ngày
CHANNEL_MONTHLY = 1450690861036994763    # Bảng xếp hạng tháng - ngày 1 và 15 lúc 2h50

# Múi giờ Việt Nam
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

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
        
        # Khởi tạo tasks
        self.auto_post_daily_task = None
        self.auto_post_weekly_task = None
        self.auto_post_monthly_task = None
        
    async def setup_hook(self):
        """Thiết lập bot khi khởi động"""
        print("🤖 Bot bảng xếp hạng đang thiết lập...")
        print("⚠️ Bỏ qua sync commands (sẽ dùng commands đã sync trước đó)")
        print("✅ Setup hook hoàn tất")
    
    async def on_ready(self):
        """Khi bot sẵn sàng"""
        try:
            print(f"🎉 {self.user} đã online!")
            print(f"🏆 Bot bảng xếp hạng sẵn sàng")
            print(f"🎯 Server được phép: {ALLOWED_SERVER_ID}")
            
            # Set status
            print("📝 Đang set status...")
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="bảng xếp hạng 🏆"
                )
            )
            print("✅ Đã set status")
            
            # Khởi động scheduled tasks
            print("⏰ Checking tasks...")
            if not self.auto_post_daily_task:
                print("⏰ Đang khởi động scheduled tasks...")
                try:
                    self.auto_post_daily_task = self.loop.create_task(self.auto_post_daily_loop())
                    self.auto_post_weekly_task = self.loop.create_task(self.auto_post_weekly_loop())
                    self.auto_post_monthly_task = self.loop.create_task(self.auto_post_monthly_loop())
                    print("✅ Đã khởi động tất cả scheduled tasks")
                except Exception as e:
                    print(f"❌ Lỗi khởi động tasks: {e}")
                    import traceback
                    traceback.print_exc()
            
            print("✅ on_ready hoàn tất")
            
        except Exception as e:
            print(f"❌ Lỗi trong on_ready: {e}")
            import traceback
            traceback.print_exc()
    
    async def on_guild_join(self, guild):
        """Khi bot join server mới"""
        if guild.id != ALLOWED_SERVER_ID:
            print(f"⚠️ Bot join server không được phép: {guild.name} ({guild.id})")
            print("🚪 Đang rời server...")
            await guild.leave()
        else:
            print(f"✅ Bot join server được phép: {guild.name}")
    
    # ==================== SCHEDULED TASKS ====================
    
    async def auto_post_daily_loop(self):
        """Tự động gửi bảng xếp hạng ngày lúc 2h58 sáng"""
        try:
            await self.wait_until_ready()
            print("✅ Task ngày đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    now = datetime.now(VN_TZ)
                    
                    # Kiểm tra xem có phải 2h58 không
                    if now.hour == 2 and now.minute == 58:
                        print("⏰ [AUTO] Đang gửi bảng xếp hạng ngày...")
                        channel = self.get_channel(CHANNEL_DAILY)
                        if channel:
                            await self.send_leaderboard_to_channel(channel, "day", "hôm qua")
                            print("✅ [AUTO] Đã gửi bảng xếp hạng ngày")
                        else:
                            print(f"❌ Không tìm thấy channel {CHANNEL_DAILY}")
                        
                        # Đợi 2 phút để tránh gửi lại
                        await asyncio.sleep(120)
                    else:
                        # Kiểm tra lại sau 30 giây
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ [AUTO] Lỗi task ngày: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            print(f"❌ [FATAL] Task ngày crashed: {e}")
            import traceback
            traceback.print_exc()
    
    async def auto_post_weekly_loop(self):
        """Tự động gửi bảng xếp hạng tuần lúc 20h và 2h55"""
        try:
            await self.wait_until_ready()
            print("✅ Task tuần đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    now = datetime.now(VN_TZ)
                    
                    # Kiểm tra xem có phải 20h00 hoặc 2h55 không
                    if (now.hour == 20 and now.minute == 0) or (now.hour == 2 and now.minute == 55):
                        print(f"⏰ [AUTO] Đang gửi bảng xếp hạng tuần ({now.hour}h{now.minute:02d})...")
                        channel = self.get_channel(CHANNEL_WEEKLY)
                        if channel:
                            await self.send_leaderboard_to_channel(channel, "week", "tuần này")
                            print("✅ [AUTO] Đã gửi bảng xếp hạng tuần")
                        else:
                            print(f"❌ Không tìm thấy channel {CHANNEL_WEEKLY}")
                        
                        # Đợi 2 phút để tránh gửi lại
                        await asyncio.sleep(120)
                    else:
                        # Kiểm tra lại sau 30 giây
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ [AUTO] Lỗi task tuần: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            print(f"❌ [FATAL] Task tuần crashed: {e}")
            import traceback
            traceback.print_exc()
    
    async def auto_post_monthly_loop(self):
        """Tự động gửi bảng xếp hạng tháng vào ngày 1 và 15 lúc 2h50"""
        try:
            await self.wait_until_ready()
            print("✅ Task tháng đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    now = datetime.now(VN_TZ)
                    
                    # Kiểm tra xem có phải ngày 1 hoặc 15 lúc 2h50 không
                    if (now.day == 1 or now.day == 15) and now.hour == 2 and now.minute == 50:
                        print(f"⏰ [AUTO] Đang gửi bảng xếp hạng tháng (ngày {now.day})...")
                        channel = self.get_channel(CHANNEL_MONTHLY)
                        if channel:
                            await self.send_leaderboard_to_channel(channel, "month", "tháng này")
                            print("✅ [AUTO] Đã gửi bảng xếp hạng tháng")
                        else:
                            print(f"❌ Không tìm thấy channel {CHANNEL_MONTHLY}")
                        
                        # Đợi 2 phút để tránh gửi lại
                        await asyncio.sleep(120)
                    else:
                        # Kiểm tra lại sau 30 giây
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ [AUTO] Lỗi task tháng: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            print(f"❌ [FATAL] Task tháng crashed: {e}")
            import traceback
            traceback.print_exc()
    
    async def send_leaderboard_to_channel(self, channel, period_type: str, period_name: str):
        """Gửi bảng xếp hạng vào channel"""
        try:
            # Lấy dữ liệu từ API
            leaderboard_data = await fetch_leaderboard_data(period_type)
            
            if not leaderboard_data:
                await channel.send(f"❌ Không thể lấy dữ liệu bảng xếp hạng {period_name}!")
                return
            
            # Render ảnh bảng xếp hạng
            image_data = await render_leaderboard_image(leaderboard_data)
            
            if image_data:
                # Gửi ảnh
                file = discord.File(
                    fp=BytesIO(image_data),
                    filename="leaderboard.png"
                )
                
                period_info = get_period_info(period_type)
                await channel.send(
                    content=f"🏆 **Bảng Xếp Hạng Học Tập** - Top 10 người học chăm chỉ nhất {period_info}!",
                    file=file
                )
            else:
                # Fallback: gửi text
                leaderboard_text = f"🏆 **Bảng Xếp Hạng Học Tập {period_name.title()}**\n\n"
                for i, member in enumerate(leaderboard_data[:10], 1):
                    time_str = format_time(member["dayTrackTime"])
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                    leaderboard_text += f"{medal} **{member['displayName']}** - {time_str}\n"
                
                await channel.send(leaderboard_text)
                
        except Exception as e:
            print(f"❌ Lỗi gửi bảng xếp hạng: {e}")
            import traceback
            traceback.print_exc()

def format_time(seconds):
    """Chuyển đổi giây thành định dạng giờ:phút:giây"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def get_period_info(period_type):
    """Lấy thông tin khoảng thời gian theo múi giờ Việt Nam"""
    # Múi giờ Việt Nam (UTC+7)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    if period_type == "day":
        # Hôm nay
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return f"hôm nay ({start_date.strftime('%d/%m/%Y')})"
    
    elif period_type == "week":
        # Tuần này (từ thứ 2 đến chủ nhật)
        days_since_monday = now.weekday()  # 0 = Monday, 6 = Sunday
        start_of_week = now - timedelta(days=days_since_monday)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        return f"tuần này ({start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')})"
    
    elif period_type == "month":
        # Tháng này
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Tháng sau, ngày 1, rồi trừ 1 ngày để có ngày cuối tháng này
        if now.month == 12:
            next_month = start_of_month.replace(year=now.year + 1, month=1)
        else:
            next_month = start_of_month.replace(month=now.month + 1)
        end_of_month = next_month - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59)
        
        return f"tháng {now.month}/{now.year} ({start_of_month.strftime('%d/%m')} - {end_of_month.strftime('%d/%m/%Y')})"
    
    else:
        return period_type

def get_period_info(period_type):
    """Lấy thông tin khoảng thời gian theo múi giờ Việt Nam"""
    # Múi giờ Việt Nam (UTC+7)
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    if period_type == "day":
        # Hôm nay
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        return f"hôm nay ({start_date.strftime('%d/%m/%Y')})"
    
    elif period_type == "week":
        # Tuần này (từ thứ 2 đến chủ nhật)
        days_since_monday = now.weekday()  # 0 = Monday, 6 = Sunday
        start_of_week = now - timedelta(days=days_since_monday)
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)
        
        return f"tuần này ({start_of_week.strftime('%d/%m')} - {end_of_week.strftime('%d/%m/%Y')})"
    
    elif period_type == "month":
        # Tháng này
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Tháng sau, ngày 1, rồi trừ 1 ngày để có ngày cuối tháng này
        if now.month == 12:
            next_month = start_of_month.replace(year=now.year + 1, month=1)
        else:
            next_month = start_of_month.replace(month=now.month + 1)
        end_of_month = next_month - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59)
        
        return f"tháng {now.month}/{now.year} ({start_of_month.strftime('%d/%m')} - {end_of_month.strftime('%d/%m/%Y')})"
    
    else:
        return period_type

def clean_username(username):
    """Loại bỏ emoji khỏi tên người dùng, giữ lại ký tự đặc biệt"""
    if not username:
        return "Unknown User"
    
    # Loại bỏ emoji bằng regex
    # Pattern này sẽ loại bỏ hầu hết emoji Unicode
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+", 
        flags=re.UNICODE
    )
    
    # Chỉ loại bỏ emoji, giữ lại tất cả ký tự khác
    cleaned = emoji_pattern.sub('', username)
    
    # Loại bỏ khoảng trắng thừa
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Nếu tên bị xóa hết thì dùng tên mặc định
    if not cleaned or len(cleaned.strip()) == 0:
        return "User"
    
    # Giới hạn độ dài tên (tối đa 25 ký tự để giữ nhiều ký tự hơn)
    if len(cleaned) > 25:
        cleaned = cleaned[:25].strip()
    
    return cleaned

async def fetch_leaderboard_data(leaderboard_type="day"):
    """Lấy dữ liệu bảng xếp hạng từ API"""
    try:
        print(f"📡 Đang lấy dữ liệu bảng xếp hạng {leaderboard_type}...")
        
        async with aiohttp.ClientSession() as session:
            url = f"{API_BASE_URL}?type={leaderboard_type}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Đã lấy được {len(data.get('leaderboard', []))} người dùng")
                    
                    # Chuyển đổi dữ liệu API thành format bot
                    leaderboard_data = []
                    for user in data.get('leaderboard', []):
                        # Lưu avatar hash để GUI system xử lý
                        avatar_hash = user.get('avatar')
                        
                        # Tạo avatar URL cho debug (không dùng trong GUI)
                        avatar_url = None
                        if avatar_hash:
                            avatar_url = f"https://cdn.discordapp.com/avatars/{user['userId']}/{avatar_hash}.png?size=256"
                        else:
                            avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"
                        
                        # Chuyển đổi studyTime từ milliseconds sang giây
                        study_time_seconds = user['studyTime'] // 1000  # Chia 1000 để chuyển từ ms sang giây
                        
                        # Làm sạch tên người dùng (loại bỏ emoji)
                        clean_name = clean_username(user['userName'])
                        
                        leaderboard_data.append({
                            "displayName": clean_name,  # Tên đã được làm sạch
                            "dayTrackTime": study_time_seconds,
                            "avatarURL": avatar_url,  # Để debug
                            "avatarHash": avatar_hash,  # Để GUI system sử dụng
                            "userId": user['userId']
                        })
                    
                    return leaderboard_data
                else:
                    print(f"❌ API trả về lỗi: {response.status}")
                    return None
                    
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu API: {e}")
        return None

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
            # Lấy user ID và avatar hash từ API
            user_id = int(member["userId"]) if member.get("userId") else i
            avatar_hash = member.get("avatarHash")  # Lấy hash trực tiếp từ API
            
            print(f"👤 User {i}: {member['displayName']} - ID: {user_id} - Avatar: {avatar_hash}")
            
            entries.append((
                user_id,  # userid thật từ API
                i,  # position
                member["dayTrackTime"],  # time in seconds
                member["displayName"],  # name
                (user_id, avatar_hash)  # avatar_key với hash thật
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
async def leaderboard_day_command(interaction: discord.Interaction):
    """Lệnh bảng xếp hạng ngày"""
    period_info = get_period_info("day")
    await leaderboard_command(interaction, "day", period_info)

@bot.tree.command(name="bangxephang-tuan", description="Xem bảng xếp hạng học tập tuần này")
async def leaderboard_week_command(interaction: discord.Interaction):
    """Lệnh bảng xếp hạng tuần"""
    period_info = get_period_info("week")
    await leaderboard_command(interaction, "week", period_info)

@bot.tree.command(name="bangxephang-thang", description="Xem bảng xếp hạng học tập tháng này")
async def leaderboard_month_command(interaction: discord.Interaction):
    """Lệnh bảng xếp hạng tháng"""
    period_info = get_period_info("month")
    await leaderboard_command(interaction, "month", period_info)

async def leaderboard_command(interaction: discord.Interaction, period_type: str, period_name: str):
    """Lệnh bảng xếp hạng chung"""
    # Respond ngay lập tức để tránh timeout
    await interaction.response.send_message(f"🎨 Đang tạo bảng xếp hạng {period_name}...", ephemeral=True)
    
    try:
        # Lấy dữ liệu từ API
        print(f"🎨 Đang lấy dữ liệu bảng xếp hạng {period_type}...")
        leaderboard_data = await fetch_leaderboard_data(period_type)
        
        if not leaderboard_data:
            await interaction.channel.send("❌ Không thể lấy dữ liệu bảng xếp hạng! Vui lòng thử lại sau.")
            return
        
        # Render ảnh bảng xếp hạng
        print("🎨 Đang render bảng xếp hạng...")
        image_data = await render_leaderboard_image(leaderboard_data)
        
        if image_data:
            print(f"📊 Đã nhận image data: {len(image_data)} bytes")
            
            # Gửi ảnh dạng tin nhắn thường (không embed)
            file = discord.File(
                fp=BytesIO(image_data),
                filename="leaderboard.png"
            )
            
            # Gửi tin nhắn mới thay vì followup
            await interaction.channel.send(
                content=f"🏆 **Bảng Xếp Hạng Học Tập** - Top 10 người học chăm chỉ nhất {period_name}!",
                file=file
            )
            print("✅ Đã gửi bảng xếp hạng với ảnh")
            
        else:
            print("⚠️ Không có image data, gửi fallback text")
            # Fallback: gửi text nếu không render được ảnh
            leaderboard_text = f"🏆 **Bảng Xếp Hạng Học Tập {period_name.title()}**\n\n"
            for i, member in enumerate(leaderboard_data[:10], 1):
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

def main():
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
    print("🏆 Chức năng: Bảng xếp hạng từ API")
    print("🎨 GUI: Có hỗ trợ render ảnh")
    print("📡 API: ", API_BASE_URL)
    print("=" * 40)
    
    try:
        bot.run(token)
    except KeyboardInterrupt:
        print("\n🛑 Đang tắt bot...")
    except Exception as e:
        print(f"❌ Lỗi khởi động bot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()