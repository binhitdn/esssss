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
import time
from datetime import datetime, timedelta, time
import pytz
from io import BytesIO

import random

# Force UTF-8 encoding for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# API endpoint
API_BASE_URL = "https://api.14study.io.vn/api/leaderboard/top-learners"

# Server ID được phép
ALLOWED_SERVER_ID = 1434581250798125068

# Channel IDs cho auto-post
CHANNEL_DAILY = 1450690801934930124      # Bảng xếp hạng ngày - 2h58 mỗi ngày
CHANNEL_WEEKLY = 1435035898629591040     # Bảng xếp hạng tuần - 20h và 2h55 mỗi ngày
CHANNEL_MONTHLY = 1450690861036994763    # Bảng xếp hạng tháng - ngày 1 và 15 lúc 2h50

# Channel ID cho đánh thức học tập
WAKEUP_CHANNEL = 1456243735938600970     # Channel đánh thức học tập

# Category ID cho phòng học đếm ngược
STUDY_ROOMS_CATEGORY = 1436215086694924449  # Danh mục phòng học đếm ngược

# Múi giờ Việt Nam
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')

class LeaderboardBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.presences = True
        
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
        
        # Kiểm tra có cần sync commands không
        import os
        if os.path.exists('.sync_commands'):
            print("🔄 Đang sync slash commands...")
            try:
                synced = await self.tree.sync()
                print(f"✅ Đã sync {len(synced)} slash commands")
                # Xóa file sau khi sync thành công
                os.remove('.sync_commands')
            except Exception as e:
                print(f"❌ Lỗi sync commands: {e}")
        else:
            print("⚠️ Bỏ qua sync commands (sẽ dùng commands đã sync trước đó)")
            print("💡 Tạo file '.sync_commands' để sync lần khởi động tiếp theo")
        
        print("✅ Setup hook hoàn tất")
    
    async def on_ready(self):
        """Khi bot sẵn sàng"""
        try:
            print(f"🎉 {self.user} đã online!")
            print(f"🏆 Bot bảng xếp hạng sẵn sàng")
            print(f"🎯 Server được phép: {ALLOWED_SERVER_ID}")
            
            # Set status to offline (invisible)
            print("📝 Đang set status offline...")
            await self.change_presence(status=discord.Status.invisible)
            print("✅ Đã set status offline")
            
            # Kiểm tra và rời khỏi các server không được phép
            print("🕵️ Đang kiểm tra danh sách server...")
            for guild in self.guilds:
                if guild.id != ALLOWED_SERVER_ID:
                    print(f"⚠️ Phát hiện server không được phép: {guild.name} ({guild.id})")
                    print("🚪 Đang rời server...")
                    await guild.leave()
            
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
                # Tạo nội dung text
                leaderboard_text = generate_leaderboard_text(leaderboard_data, period_type, period_name)
                
                # Gửi ảnh và text
                file = discord.File(
                    fp=BytesIO(image_data),
                    filename="leaderboard.png"
                )
                
                await channel.send(
                    content=leaderboard_text,
                    file=file
                )
            else:
                # Fallback: gửi text
                leaderboard_text = generate_leaderboard_text(leaderboard_data, period_type, period_name)
                
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

def format_duration_vietnamese(seconds):
    """Chuyển đổi giây thành định dạng XX giờ YY phút"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours:02d} giờ {minutes:02d} phút"

def generate_leaderboard_text(data, period_type, period_name):
    """Tạo nội dung text cho bảng xếp hạng theo yêu cầu"""
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    # Kiểm tra xem có phải khung giờ báo cáo (2h-3h sáng) hay không
    is_reporting_hour = 2 <= now.hour < 3
    
    date_str_footer = ""
    title = ""
    
    if period_type == "day":
        if is_reporting_hour:
            # Báo cáo tổng kết ngày hôm qua
            display_date = now - timedelta(days=1)
            date_str = display_date.strftime("%d/%m/%Y")
            title = f"TOP 10 HỌC VIÊN XUẤT SẮC NGÀY {date_str}"
            date_str_footer = f"Ngày {date_str}"
        else:
            # Báo cáo tạm tính trong ngày
            # Logic cũ: trước 3h sáng thì vẫn coi là ngày hôm qua (nghĩa là đang trong ngày học cũ)
            # Nhưng theo yêu cầu mới: "Nếu không thì bxh ngày ... tính đến..."
            # Nếu đang là 10h sáng -> bxh ngày hôm nay tính đến 10h
            # Nếu đang là 1h sáng -> bxh ngày hôm qua tính đến 1h sáng (vì chưa qua mốc 3h)
            
            if now.hour < 3:
                display_date = now - timedelta(days=1)
            else:
                display_date = now
                
            date_str = display_date.strftime("%d/%m/%Y")
            title = f"TOP 10 HỌC VIÊN XUẤT SẮC NGÀY {date_str}"
            date_str_footer = f"Số liệu tính đến {now.strftime('%H:%M')} ngày {now.strftime('%d/%m')}"

    elif period_type == "week":
        # Monday = 0
        if now.weekday() == 0 and is_reporting_hour:
            # Báo cáo tổng kết tuần trước (vào thứ 2 lúc 2h-3h)
            title = "TOP 10 HỌC VIÊN XUẤT SẮC TUẦN TRƯỚC"
            end_of_last_week = now - timedelta(days=1) # CN hôm qua
            start_of_last_week = end_of_last_week - timedelta(days=6)
            date_str_footer = f"Tuần {start_of_last_week.strftime('%d/%m')} - {end_of_last_week.strftime('%d/%m/%Y')}"
        else:
            # Báo cáo tuần này (tạm tính)
            title = "TOP 10 HỌC VIÊN XUẤT SẮC TUẦN NÀY"
            # Cần tính tuần hiện tại của "ngày học"
            # Nếu đang là thứ 2 lúc 1h sáng -> vẫn thuộc tuần trước?
            # Theo logic 3AM cutoff:
            current_study_date = now
            if now.hour < 3:
                current_study_date = now - timedelta(days=1)
                
            # Tìm thứ 2 của tuần chứa current_study_date
            days_since_monday = current_study_date.weekday()
            start_of_week = current_study_date - timedelta(days=days_since_monday)
            end_of_week = start_of_week + timedelta(days=6)
            
            date_str_footer = f"Số liệu tính đến {now.strftime('%H:%M')} ngày {now.strftime('%d/%m')}"

    elif period_type == "month":
        # Day 1
        if now.day == 1 and is_reporting_hour:
            # Báo cáo tổng kết tháng trước (vào ngày 1 lúc 2h-3h)
            last_month = now - timedelta(days=1)
            title = f"TOP 10 HỌC VIÊN XUẤT SẮC THÁNG {last_month.month}/{last_month.year}"
            date_str_footer = f"Tháng {last_month.month}/{last_month.year}"
        else:
            # Báo cáo tháng này (tạm tính)
            # Cần tính tháng của "ngày học"
            current_study_date = now
            if now.hour < 3:
                current_study_date = now - timedelta(days=1)
                
            title = f"TOP 10 HỌC VIÊN XUẤT SẮC THÁNG {current_study_date.month}/{current_study_date.year}"
            date_str_footer = f"Số liệu tính đến {now.strftime('%H:%M')} ngày {now.strftime('%d/%m')}"
            
    else:
        title = f"TOP 10 HỌC VIÊN XUẤT SẮC {period_name.upper()}"
        date_str_footer = now.strftime("%d/%m/%Y")

    text = f"**{title}**\n\n"

    # Top 10 list
    # Format: 1. 3h 45p: <@userId>
    for i, member in enumerate(data[:10], 1):
        time_str = format_duration_vietnamese(member["dayTrackTime"])
        
        # Sử dụng mention tag <@userId>
        user_id = member.get('userId')
        if user_id:
            mention = f"<@{user_id}>"
        else:
            mention = f"@{member['displayName']}"
        
        if i == 1:
            prefix = "🥇"
        elif i == 2:
            prefix = "🥈"
        elif i == 3:
            prefix = "🥉" 
        else:
            prefix = "🔹"

        # Format: Icon Time: User
        # Loại bỏ số thứ tự thừa, không xuống dòng thừa
        if i <= 3:
            text += f"**{prefix} {time_str}: {mention}**\n"
        else:
            text += f"{prefix} {time_str}: {mention}\n"

    # Date info
    text += f"\n**{date_str_footer}**\n\n"
    
    # Motivational Footer
    text += "Tiếp tục phát huy! Tháng sau sẽ có những kỷ lục mới! 🚀"
    
    return text

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
    """Lấy dữ liệu bảng xếp hạng từ API với cơ chế retry"""
    retry_count = 5
    base_delay = 2
    
    for attempt in range(retry_count):
        try:
            print(f"📡 Đang lấy dữ liệu bảng xếp hạng {leaderboard_type} (Lần {attempt + 1}/{retry_count})...")
            
            async with aiohttp.ClientSession() as session:
                url = f"{API_BASE_URL}?type={leaderboard_type}"
                # Headers để tránh bị chặn (quan trọng là Referer)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "application/json",
                    "Referer": "https://14study.io.vn/"
                }
                # Timeout cho request là 10 giây
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Kiểm tra dữ liệu có hợp lệ không
                        if not data or 'leaderboard' not in data:
                            print(f"⚠️ Dữ liệu API trả về không hợp lệ (Lần {attempt + 1})")
                            raise ValueError("Invalid API response format")
                            
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
                        print(f"❌ API trả về lỗi: {response.status} (Lần {attempt + 1})")
                        # Nếu lỗi 404 hoặc 403 thì có thể không cần retry, nhưng tạm thời cứ retry cho chắc
        
        except Exception as e:
            print(f"⚠️ Lỗi khi lấy dữ liệu API (Lần {attempt + 1}): {e}")
        
        # Nếu chưa phải lần cuối thì chờ rồi thử lại
        if attempt < retry_count - 1:
            delay = base_delay * (2 ** attempt)  # 2, 4, 8, 16...
            print(f"⏳ Đợi {delay} giây trước khi thử lại...")
            await asyncio.sleep(delay)
            
    print("❌ Đã hết số lần thử lại. Không lấy được dữ liệu.")
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
        
        image_data = None
        retry_count = 3
        
        for attempt in range(retry_count):
            try:
                if attempt > 0:
                    print(f"🔄 Render attempt {attempt + 1}/{retry_count}...")
                
                image_data = await gui_client.request(
                    route='leaderboard_card',
                    args=(),
                    kwargs={
                        'server_name': '14 hours a day(STUDY VIP)',
                        'entries': entries,
                        'highlight': None,
                        'locale': 'vi'
                    },
                    timeout=300  # Explicit 5 minutes timeout
                )
                
                if image_data:
                    break
                    
            except asyncio.TimeoutError:
                print(f"⚠️ Render attempt {attempt + 1} TIMED OUT (>300s)")
                if attempt < retry_count - 1:
                    await asyncio.sleep(5)
            except Exception as e:
                print(f"⚠️ Render attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    await asyncio.sleep(5)
        
        if image_data:
            print(f"✅ Render thành công: {len(image_data)} bytes")
            
            # Upscale ảnh lên 2x để hiển thị to hơn trên Discord
            try:
                from PIL import Image
                with BytesIO(image_data) as bio:
                    img = Image.open(bio)
                    # Resize x2
                    new_size = (int(img.width * 2), int(img.height * 2))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                    
                    # Save back to bytes
                    out_bio = BytesIO()
                    img.save(out_bio, format='PNG')
                    image_data = out_bio.getvalue()
                    print(f"✅ Đã upscale ảnh: {new_size} - {len(image_data)} bytes")
            except Exception as e:
                print(f"⚠️ Không thể upscale ảnh: {e}")
                
            return image_data
        else:
            return None
                    
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

@bot.tree.command(name="test-leaderboard", description="🧪 [ADMIN] Test gửi bảng xếp hạng ngay")
async def test_leaderboard_command(interaction: discord.Interaction, period_type: str = "day"):
    """Test gửi bảng xếp hạng"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    if period_type not in ["day", "week", "month"]:
        await interaction.response.send_message("❌ Period type phải là: day, week, hoặc month", ephemeral=True)
        return
    
    await interaction.response.send_message(f"🧪 Đang test gửi bảng xếp hạng {period_type}...", ephemeral=True)
    
    try:
        await bot.send_leaderboard_to_channel(interaction.channel, period_type, f"{period_type} (test)")
        await interaction.followup.send(f"✅ Đã test gửi bảng xếp hạng {period_type}!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Lỗi test leaderboard: {e}", ephemeral=True)

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
            
            # Tạo nội dung text
            leaderboard_text = generate_leaderboard_text(leaderboard_data, period_type, period_name)
            
            # Gửi ảnh dạng tin nhắn thường (không embed)
            file = discord.File(
                fp=BytesIO(image_data),
                filename="leaderboard.png"
            )
            
            # Gửi tin nhắn mới thay vì followup
            await interaction.channel.send(
                content=leaderboard_text,
                file=file
            )
            print("✅ Đã gửi bảng xếp hạng với ảnh và text")
            
        else:
            print("⚠️ Không có image data, gửi fallback text")
            # Fallback: gửi text
            leaderboard_text = generate_leaderboard_text(leaderboard_data, period_type, period_name)
            
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