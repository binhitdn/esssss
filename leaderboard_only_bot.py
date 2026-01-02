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

# Warning system
WARNING_ROLE_ID = 1436409040036040886        # Role ID cần tag warning (thay đổi từ user ID)
WARNING_CHANNEL_ID = 1446655389860106361     # Channel gửi warning

# PendingKick system
PENDINGKICK_ROLE_ID = 1436802180429385768    # Role ID PendingKick
PENDINGKICK_CHANNEL_ID = 1446655276962021497 # Channel gửi PendingKick

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
        
        # Cooldown cho đánh thức (tránh spam)
        self.wakeup_cooldown = {}
        self.wakeup_cooldown_duration = 300  # 5 phút
        
        # Lưu trữ thông tin phòng đếm ngược
        self.countdown_rooms = {}  # {channel_id: {'name': str, 'target_date': datetime, 'creator_id': int, 'format_type': str}}
        self.countdown_update_task = None
        
        # Lưu trữ tin nhắn warning để xóa sau
        self.warning_messages = {}  # {message_id: {'delete_time': datetime, 'channel_id': int}}
        
        # Lưu trữ tin nhắn pendingkick để xóa sau
        self.pendingkick_messages = {}  # {message_id: {'delete_time': datetime, 'channel_id': int}}
        
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
                    
                    # Khởi động countdown update task
                    self.countdown_update_task = self.loop.create_task(self.countdown_update_loop())
                    
                    # Khởi động warning system task
                    self.warning_task = self.loop.create_task(self.warning_system_loop())
                    
                    # Khởi động pendingkick system task
                    self.pendingkick_task = self.loop.create_task(self.pendingkick_system_loop())
                    
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
    
    # ==================== COUNTDOWN ROOM LOOP ====================
    
    async def countdown_update_loop(self):
        """Cập nhật tên phòng đếm ngược mỗi phút"""
        try:
            await self.wait_until_ready()
            print("✅ Countdown update task đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    if self.countdown_rooms:
                        print(f"🔄 Cập nhật {len(self.countdown_rooms)} phòng đếm ngược...")
                        
                        rooms_to_remove = []
                        
                        for channel_id, room_info in self.countdown_rooms.items():
                            channel = self.get_channel(channel_id)
                            if not channel:
                                rooms_to_remove.append(channel_id)
                                continue
                            
                            # Tính toán thời gian còn lại
                            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                            now = datetime.now(vn_tz)
                            target_date = room_info['target_date']
                            
                            # Đảm bảo target_date có timezone
                            if target_date.tzinfo is None:
                                target_date = vn_tz.localize(target_date)
                            
                            time_left = target_date - now
                            
                            if time_left.total_seconds() <= 0:
                                # Hết thời gian - xóa phòng
                                print(f"⏰ Phòng {room_info['name']} đã hết thời gian, đang xóa...")
                                
                                # Gửi thông báo cuối
                                try:
                                    await channel.send(f"🎉 **ĐÃ ĐẾN NGÀY {room_info['name'].upper()}!** 🎉\n\nPhòng này sẽ tự động xóa sau 30 giây...")
                                    await asyncio.sleep(30)
                                    await channel.delete(reason="Countdown finished")
                                except Exception as e:
                                    print(f"❌ Lỗi xóa phòng {channel_id}: {e}")
                                
                                rooms_to_remove.append(channel_id)
                            else:
                                # Cập nhật tên phòng
                                new_name = generate_countdown_name(room_info['name'], time_left, room_info['format_type'])
                                
                                if channel.name != new_name:
                                    try:
                                        await channel.edit(name=new_name, reason="Countdown update")
                                        print(f"✅ Cập nhật phòng: {new_name}")
                                    except Exception as e:
                                        print(f"❌ Lỗi cập nhật tên phòng {channel_id}: {e}")
                        
                        # Xóa các phòng đã hết hạn
                        for channel_id in rooms_to_remove:
                            del self.countdown_rooms[channel_id]
                    
                    # Đợi 60 giây trước khi cập nhật tiếp
                    await asyncio.sleep(300)  # 5 phút = 300 giây
                    
                except Exception as e:
                    print(f"❌ [COUNTDOWN] Lỗi update loop: {e}")
                    await asyncio.sleep(300)  # 5 phút nếu có lỗi
                    
        except Exception as e:
            print(f"❌ [FATAL] Countdown update task crashed: {e}")
            import traceback
            traceback.print_exc()
    
    # ==================== WARNING SYSTEM ====================
    
    async def warning_system_loop(self):
        """Hệ thống cảnh báo tự động"""
        try:
            await self.wait_until_ready()
            print("✅ Warning system task đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                    now = datetime.now(vn_tz)
                    
                    # Kiểm tra gửi warning lúc 6h sáng
                    if now.hour == 6 and now.minute == 0:
                        print("⚠️ [WARNING] Đang gửi cảnh báo 6h sáng...")
                        await self.send_warning_message()
                        
                        # Đợi 2 phút để tránh gửi lại
                        await asyncio.sleep(120)
                    
                    # Kiểm tra xóa tin nhắn warning lúc 2h51
                    elif now.hour == 2 and now.minute == 51:
                        print("🗑️ [WARNING] Đang xóa tin nhắn cảnh báo...")
                        await self.delete_warning_messages()
                        
                        # Đợi 2 phút để tránh xử lý lại
                        await asyncio.sleep(120)
                    
                    else:
                        # Kiểm tra lại sau 30 giây
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ [WARNING] Lỗi warning system: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            print(f"❌ [FATAL] Warning system crashed: {e}")
            import traceback
            traceback.print_exc()
    
    async def send_warning_message(self):
        """Gửi tin nhắn cảnh báo lúc 6h sáng"""
        try:
            # Lấy channel
            channel = self.get_channel(WARNING_CHANNEL_ID)
            if not channel:
                print(f"❌ Không tìm thấy channel warning {WARNING_CHANNEL_ID}")
                return
            
            # Lấy guild để tìm role
            guild = channel.guild
            role = guild.get_role(WARNING_ROLE_ID)
            if not role:
                print(f"❌ Không tìm thấy role Warning {WARNING_ROLE_ID}")
                return
            
            # Lấy danh sách members có role Warning
            warning_members = [member for member in guild.members if role in member.roles]
            
            if not warning_members:
                print("📭 [WARNING] Không có thành viên nào có role Warning")
                return
            
            # Tạo danh sách mentions
            member_mentions = " ".join([member.mention for member in warning_members])
            
            # Tính ngày mai
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            tomorrow = datetime.now(vn_tz) + timedelta(days=1)
            tomorrow_str = tomorrow.strftime('%d/%m/%Y')
            
            # Tạo nội dung warning nhẹ nhàng hơn
            warning_content = f"""
⚠️ **NHẮC NHỞ HỌC TẬP** ⚠️

{member_mentions}

Cậu đã được gắn **Warning** vì vậy hãy học đủ thời gian mục tiêu trước **3h sáng ngày {tomorrow_str}** trước khi bị chuyển sang **PendingKick**.

📊 **Để biết thời gian mục tiêu của mình là bao nhiêu:**
🔗 Truy cập: https://14study.io.vn

⚠️ **Lưu ý:** Nếu cậu không cài đặt thì mặc định là **1 giờ**.

🎯 **Hãy cố gắng học tập để tiếp tục ở lại với mọi người nhé!**

---
*Tin nhắn này sẽ tự động xóa vào 2h51 sáng ngày mai.*
"""
            
            # Gửi tin nhắn
            message = await channel.send(warning_content)
            
            # Tính thời gian xóa (2h51 sáng ngày mai)
            delete_time = tomorrow.replace(hour=2, minute=51, second=0, microsecond=0)
            
            # Lưu thông tin để xóa sau
            self.warning_messages[message.id] = {
                'delete_time': delete_time,
                'channel_id': channel.id,
                'sent_time': datetime.now(vn_tz),
                'member_count': len(warning_members)
            }
            
            print(f"✅ [WARNING] Đã gửi nhắc nhở cho {len(warning_members)} thành viên (Message ID: {message.id})")
            print(f"🗑️ [WARNING] Sẽ xóa lúc: {delete_time.strftime('%H:%M %d/%m/%Y')}")
            
        except Exception as e:
            print(f"❌ [WARNING] Lỗi gửi nhắc nhở: {e}")
            import traceback
            traceback.print_exc()
    
    async def delete_warning_messages(self):
        """Xóa tin nhắn cảnh báo lúc 2h51"""
        try:
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(vn_tz)
            
            messages_to_delete = []
            
            for message_id, info in self.warning_messages.items():
                # Kiểm tra xem có đến giờ xóa chưa
                if now >= info['delete_time']:
                    messages_to_delete.append(message_id)
            
            if not messages_to_delete:
                print("📭 [WARNING] Không có tin nhắn nào cần xóa")
                return
            
            deleted_count = 0
            
            for message_id in messages_to_delete:
                try:
                    info = self.warning_messages[message_id]
                    channel = self.get_channel(info['channel_id'])
                    
                    if channel:
                        message = await channel.fetch_message(message_id)
                        await message.delete()
                        deleted_count += 1
                        print(f"✅ [WARNING] Đã xóa tin nhắn {message_id}")
                    
                    # Xóa khỏi danh sách theo dõi
                    del self.warning_messages[message_id]
                    
                except discord.NotFound:
                    print(f"⚠️ [WARNING] Tin nhắn {message_id} đã bị xóa trước đó")
                    del self.warning_messages[message_id]
                except Exception as e:
                    print(f"❌ [WARNING] Lỗi xóa tin nhắn {message_id}: {e}")
            
            print(f"🗑️ [WARNING] Đã xóa {deleted_count} tin nhắn cảnh báo")
            
        except Exception as e:
            print(f"❌ [WARNING] Lỗi xóa tin nhắn: {e}")
            import traceback
            traceback.print_exc()
    
    # ==================== PENDINGKICK SYSTEM ====================
    
    async def pendingkick_system_loop(self):
        """Hệ thống PendingKick tự động"""
        try:
            await self.wait_until_ready()
            print("✅ PendingKick system task đã sẵn sàng")
            
            while not self.is_closed():
                try:
                    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                    now = datetime.now(vn_tz)
                    
                    # Kiểm tra gửi pendingkick lúc 6h sáng
                    if now.hour == 6 and now.minute == 0:
                        print("🚨 [PENDINGKICK] Đang gửi thông báo PendingKick 6h sáng...")
                        await self.send_pendingkick_message()
                        
                        # Đợi 2 phút để tránh gửi lại
                        await asyncio.sleep(120)
                    
                    # Kiểm tra xóa tin nhắn pendingkick lúc 2h51
                    elif now.hour == 2 and now.minute == 51:
                        print("🗑️ [PENDINGKICK] Đang xóa tin nhắn PendingKick...")
                        await self.delete_pendingkick_messages()
                        
                        # Đợi 2 phút để tránh xử lý lại
                        await asyncio.sleep(120)
                    
                    else:
                        # Kiểm tra lại sau 30 giây
                        await asyncio.sleep(30)
                        
                except Exception as e:
                    print(f"❌ [PENDINGKICK] Lỗi pendingkick system: {e}")
                    await asyncio.sleep(60)
                    
        except Exception as e:
            print(f"❌ [FATAL] PendingKick system crashed: {e}")
            import traceback
            traceback.print_exc()
    
    async def send_pendingkick_message(self):
        """Gửi tin nhắn PendingKick lúc 6h sáng"""
        try:
            # Lấy channel
            channel = self.get_channel(PENDINGKICK_CHANNEL_ID)
            if not channel:
                print(f"❌ Không tìm thấy channel PendingKick {PENDINGKICK_CHANNEL_ID}")
                return
            
            # Lấy guild để tìm role
            guild = channel.guild
            role = guild.get_role(PENDINGKICK_ROLE_ID)
            if not role:
                print(f"❌ Không tìm thấy role PendingKick {PENDINGKICK_ROLE_ID}")
                return
            
            # Lấy danh sách members có role PendingKick
            pendingkick_members = [member for member in guild.members if role in member.roles]
            
            if not pendingkick_members:
                print("📭 [PENDINGKICK] Không có thành viên nào có role PendingKick")
                return
            
            # Tạo danh sách mentions
            member_mentions = " ".join([member.mention for member in pendingkick_members])
            
            # Tạo nội dung PendingKick
            pendingkick_content = f"""
🚨 **THÔNG BÁO PENDINGKICK** 🚨

{member_mentions}

Bạn đã được chuyển sang **PendingKick** do không học đủ mục tiêu **2 ngày liên tiếp**.

🔄 **Vui lòng nhấp vào nút "Xin quay lại" ở trên** nếu cậu muốn tiếp tục học với tụi mình hoặc tự rời khỏi nhóm nếu cậu không có nhu cầu ạ.

💭 **(Sẽ không có thông báo nào cho ai kể cả admin nên cậu cứ thoải mái ạ)**

---
*Tin nhắn này sẽ tự động xóa vào 2h51 sáng ngày mai.*
"""
            
            # Gửi tin nhắn
            message = await channel.send(pendingkick_content)
            
            # Tính thời gian xóa (2h51 sáng ngày mai)
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            tomorrow = datetime.now(vn_tz) + timedelta(days=1)
            delete_time = tomorrow.replace(hour=2, minute=51, second=0, microsecond=0)
            
            # Lưu thông tin để xóa sau
            self.pendingkick_messages[message.id] = {
                'delete_time': delete_time,
                'channel_id': channel.id,
                'sent_time': datetime.now(vn_tz),
                'member_count': len(pendingkick_members)
            }
            
            print(f"✅ [PENDINGKICK] Đã gửi thông báo cho {len(pendingkick_members)} thành viên (Message ID: {message.id})")
            print(f"🗑️ [PENDINGKICK] Sẽ xóa lúc: {delete_time.strftime('%H:%M %d/%m/%Y')}")
            
        except Exception as e:
            print(f"❌ [PENDINGKICK] Lỗi gửi thông báo: {e}")
            import traceback
            traceback.print_exc()
    
    async def delete_pendingkick_messages(self):
        """Xóa tin nhắn PendingKick lúc 2h51"""
        try:
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(vn_tz)
            
            messages_to_delete = []
            
            for message_id, info in self.pendingkick_messages.items():
                # Kiểm tra xem có đến giờ xóa chưa
                if now >= info['delete_time']:
                    messages_to_delete.append(message_id)
            
            if not messages_to_delete:
                print("📭 [PENDINGKICK] Không có tin nhắn nào cần xóa")
                return
            
            deleted_count = 0
            
            for message_id in messages_to_delete:
                try:
                    info = self.pendingkick_messages[message_id]
                    channel = self.get_channel(info['channel_id'])
                    
                    if channel:
                        message = await channel.fetch_message(message_id)
                        await message.delete()
                        deleted_count += 1
                        print(f"✅ [PENDINGKICK] Đã xóa tin nhắn {message_id}")
                    
                    # Xóa khỏi danh sách theo dõi
                    del self.pendingkick_messages[message_id]
                    
                except discord.NotFound:
                    print(f"⚠️ [PENDINGKICK] Tin nhắn {message_id} đã bị xóa trước đó")
                    del self.pendingkick_messages[message_id]
                except Exception as e:
                    print(f"❌ [PENDINGKICK] Lỗi xóa tin nhắn {message_id}: {e}")
            
            print(f"🗑️ [PENDINGKICK] Đã xóa {deleted_count} tin nhắn PendingKick")
            
        except Exception as e:
            print(f"❌ [PENDINGKICK] Lỗi xóa tin nhắn: {e}")
            import traceback
            traceback.print_exc()
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

# ==================== WAKEUP COMMANDS ====================

@bot.tree.command(name="danh-thuc", description="🔔 Đánh thức tất cả mọi người học tập!")
async def wakeup_all_command(interaction: discord.Interaction):
    """Đánh thức tất cả thành viên"""
    await wakeup_command(interaction, target_type="all")

@bot.tree.command(name="danh-thuc-user", description="🔔 Đánh thức một người cụ thể học tập!")
async def wakeup_user_command(interaction: discord.Interaction, user: discord.Member):
    """Đánh thức một user cụ thể"""
    await wakeup_command(interaction, target_type="user", target_user=user)

@bot.tree.command(name="danh-thuc-kenh", description="🔔 Đánh thức tất cả mọi người vào kênh đánh thức!")
async def wakeup_channel_command(interaction: discord.Interaction):
    """Đánh thức tất cả vào kênh đánh thức"""
    await wakeup_command(interaction, target_type="channel")

@bot.tree.command(name="danh-thuc-hen-gio", description="⏰ Hẹn giờ đánh thức sau X phút")
async def wakeup_timer_command(interaction: discord.Interaction, minutes: int, message: str = "Đã đến giờ học!"):
    """Hẹn giờ đánh thức"""
    if minutes < 1 or minutes > 1440:  # Tối đa 24 giờ
        await interaction.response.send_message("⚠️ Thời gian phải từ 1-1440 phút (1 ngày)!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"⏰ Đã đặt đánh thức sau {minutes} phút với nội dung: '{message}'", ephemeral=True)
    
    # Tạo task hẹn giờ
    async def delayed_wakeup():
        await asyncio.sleep(minutes * 60)
        
        # Tạo nội dung đánh thức hẹn giờ
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vn_tz)
        
        content = f"""
⏰ **ĐÁNH THỨC HẸN GIỜ** ⏰

🔔 **Thông báo từ {interaction.user.mention}**

📝 **Nội dung**: {message}
🕐 **Thời gian**: {now.strftime('%H:%M')}
⏱️ **Đã hẹn từ**: {minutes} phút trước

💪 **Đã đến lúc thực hiện cam kết của bạn!**
"""
        
        await interaction.channel.send(content)
    
    # Chạy task trong background
    bot.loop.create_task(delayed_wakeup())

@bot.tree.command(name="danh-thuc-pomodoro", description="🍅 Đánh thức Pomodoro (25p học + 5p nghỉ)")
async def wakeup_pomodoro_command(interaction: discord.Interaction, cycles: int = 1):
    """Đánh thức theo phương pháp Pomodoro"""
    if cycles < 1 or cycles > 8:
        await interaction.response.send_message("⚠️ Số chu kỳ phải từ 1-8!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"🍅 Bắt đầu {cycles} chu kỳ Pomodoro! Chúc bạn học tập hiệu quả!", ephemeral=True)
    
    # Tạo Pomodoro timer
    async def pomodoro_timer():
        for cycle in range(1, cycles + 1):
            # Bắt đầu chu kỳ học
            vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(vn_tz)
            
            start_content = f"""
🍅 **POMODORO - CHU KỲ {cycle}/{cycles}** 🍅

⏰ **BẮT ĐẦU HỌC**: {now.strftime('%H:%M')}
👤 **Người khởi tạo**: {interaction.user.mention}

📚 **25 PHÚT HỌC TẬP**
• Tập trung 100%
• Không kiểm tra điện thoại
• Không làm việc khác
• Chỉ học thôi!

⏰ **Sẽ báo nghỉ lúc**: {(now + timedelta(minutes=25)).strftime('%H:%M')}

🔥 **FOCUS MODE ON!** 🔥
"""
            await interaction.channel.send(start_content)
            
            # Đợi 25 phút
            await asyncio.sleep(25 * 60)
            
            # Báo nghỉ
            now = datetime.now(vn_tz)
            if cycle < cycles:
                break_content = f"""
🛑 **POMODORO - NGHỈ NGƠI** 🛑

⏰ **GIỜ NGHỈ**: {now.strftime('%H:%M')}
🍅 **Hoàn thành chu kỳ**: {cycle}/{cycles}

😌 **5 PHÚT NGHỈ NGƠI**
• Đứng dậy vận động
• Uống nước
• Thả lỏng mắt
• Thở sâu

⏰ **Chu kỳ tiếp theo**: {(now + timedelta(minutes=5)).strftime('%H:%M')}

💪 **Bạn đang làm rất tốt!** 💪
"""
                await interaction.channel.send(break_content)
                await asyncio.sleep(5 * 60)  # Nghỉ 5 phút
            else:
                # Kết thúc tất cả chu kỳ
                final_content = f"""
🎉 **HOÀN THÀNH POMODORO** 🎉

⏰ **Kết thúc**: {now.strftime('%H:%M')}
🍅 **Tổng chu kỳ**: {cycles}
⏱️ **Tổng thời gian học**: {cycles * 25} phút

🏆 **CHÚC MỪNG {interaction.user.mention}!**

📈 **Thành tựu hôm nay:**
• Hoàn thành {cycles} Pomodoro
• Học tập {cycles * 25} phút tập trung
• Xây dựng thói quen tốt

🎯 **Hãy tiếp tục duy trì!**
"""
                await interaction.channel.send(final_content)
    
    # Chạy Pomodoro timer
    bot.loop.create_task(pomodoro_timer())

@bot.tree.command(name="danh-thuc-stats", description="📊 Xem thống kê đánh thức của bạn")
async def wakeup_stats_command(interaction: discord.Interaction):
    """Xem thống kê đánh thức"""
    user_id = interaction.user.id
    
    # Tạo stats giả lập (trong thực tế sẽ lưu vào database)
    import random
    
    total_wakeups = random.randint(5, 50)
    wakeups_today = random.randint(0, 5)
    favorite_time = f"{random.randint(6, 22):02d}:{random.randint(0, 59):02d}"
    streak = random.randint(1, 15)
    
    stats_content = f"""
📊 **THỐNG KÊ ĐÁNH THỨC** 📊

👤 **Người dùng**: {interaction.user.mention}

📈 **Số liệu tổng quan:**
🔔 **Tổng lần đánh thức**: {total_wakeups}
📅 **Đánh thức hôm nay**: {wakeups_today}
⏰ **Giờ đánh thức yêu thích**: {favorite_time}
🔥 **Streak hiện tại**: {streak} ngày

🏆 **Thành tựu:**
{"🥇 Người đánh thức tích cực" if total_wakeups > 30 else "🥈 Người đánh thức nhiệt tình" if total_wakeups > 15 else "🥉 Người đánh thức mới"}

💪 **Động lực**: Bạn đã giúp cộng đồng học tập {total_wakeups} lần!

⭐ **Mẹo**: Đánh thức đều đặn sẽ tạo thói quen tốt cho bản thân!
"""
    
    await interaction.response.send_message(stats_content, ephemeral=True)

# ==================== COUNTDOWN ROOM COMMANDS ====================

@bot.tree.command(name="tao-phong-hoc", description="📚 Tạo phòng học đếm ngược đến ngày mục tiêu")
async def create_study_room_command(
    interaction: discord.Interaction, 
    name: str, 
    date: str, 
    format_type: str = "full_verbose"
):
    """Tạo phòng học đếm ngược
    
    Args:
        name: Tên phòng học (VD: JLPT, Thi cuối kỳ)
        date: Ngày mục tiêu (DD/MM/YYYY hoặc DD/MM/YYYY)
        format_type: Định dạng hiển thị (sẽ có dropdown select)
    """
    # Tạo dropdown select cho format
    class FormatSelect(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(
                    label="Tên + Còn xx ngày xx giờ xx phút",
                    value="full_verbose",
                    description="VD: JLPT Còn 125 ngày 22 giờ 30 phút",
                    emoji="📝"
                ),
                discord.SelectOption(
                    label="Tên + Còn xxdxxhxxp",
                    value="full_compact",
                    description="VD: JLPT Còn 125d22h30p",
                    emoji="📋"
                ),
                discord.SelectOption(
                    label="xx ngày xx giờ xx phút",
                    value="countdown_verbose",
                    description="VD: 125 ngày 22 giờ 30 phút",
                    emoji="⏰"
                ),
                discord.SelectOption(
                    label="xxdxxhxxp",
                    value="countdown_compact",
                    description="VD: 125d22h30p",
                    emoji="⏱️"
                )
            ]
            super().__init__(placeholder="Chọn định dạng hiển thị tên phòng...", options=options)
        
        async def callback(self, interaction: discord.Interaction):
            selected_format = self.values[0]
            await create_countdown_room(interaction, name, date, selected_format)
    
    class FormatView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=60)
            self.add_item(FormatSelect())
        
        async def on_timeout(self):
            # Disable all items when timeout
            for item in self.children:
                item.disabled = True
    
    # Hiển thị dropdown select
    view = FormatView()
    
    embed = discord.Embed(
        title="📚 Tạo Phòng Học Đếm Ngược",
        description=f"**Tên phòng**: {name}\n**Ngày mục tiêu**: {date}\n\n**Chọn định dạng hiển thị:**",
        color=0x3498db
    )
    
    embed.add_field(
        name="📝 Tên + Còn xx ngày xx giờ xx phút",
        value=f"`{name} Còn 125 ngày 22 giờ 30 phút`",
        inline=False
    )
    
    embed.add_field(
        name="📋 Tên + Còn xxdxxhxxp",
        value=f"`{name} Còn 125d22h30p`",
        inline=False
    )
    
    embed.add_field(
        name="⏰ xx ngày xx giờ xx phút",
        value="`125 ngày 22 giờ 30 phút`",
        inline=False
    )
    
    embed.add_field(
        name="⏱️ xxdxxhxxp",
        value="`125d22h30p`",
        inline=False
    )
    
    embed.set_footer(text="Chọn định dạng trong dropdown bên dưới • Timeout: 60 giây")
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name="xoa-phong-hoc", description="🗑️ Xóa phòng học đếm ngược của bạn")
async def delete_study_room_command(interaction: discord.Interaction):
    """Xóa phòng học đếm ngược"""
    await delete_countdown_room(interaction)

@bot.tree.command(name="danh-sach-phong-hoc", description="📋 Xem danh sách phòng học đếm ngược")
async def list_study_rooms_command(interaction: discord.Interaction):
    """Xem danh sách phòng học đếm ngược"""
    await list_countdown_rooms(interaction)

# ==================== WARNING SYSTEM COMMANDS ====================

@bot.tree.command(name="test-warning", description="🧪 [ADMIN] Test hệ thống cảnh báo")
async def test_warning_command(interaction: discord.Interaction):
    """Test hệ thống cảnh báo (chỉ admin)"""
    # Kiểm tra quyền admin (có thể thay bằng role check)
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    await interaction.response.send_message("🧪 Đang test hệ thống cảnh báo...", ephemeral=True)
    
    try:
        await bot.send_warning_message()
        await interaction.followup.send("✅ Đã gửi tin nhắn cảnh báo test!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Lỗi test warning: {e}", ephemeral=True)

@bot.tree.command(name="xoa-warning", description="🗑️ [ADMIN] Xóa tất cả tin nhắn cảnh báo")
async def delete_warning_command(interaction: discord.Interaction):
    """Xóa tất cả tin nhắn cảnh báo (chỉ admin)"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    await interaction.response.send_message("🗑️ Đang xóa tin nhắn cảnh báo...", ephemeral=True)
    
    try:
        await bot.delete_warning_messages()
        await interaction.followup.send("✅ Đã xóa tất cả tin nhắn cảnh báo!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Lỗi xóa warning: {e}", ephemeral=True)

@bot.tree.command(name="warning-status", description="📊 [ADMIN] Xem trạng thái hệ thống cảnh báo")
async def warning_status_command(interaction: discord.Interaction):
    """Xem trạng thái hệ thống cảnh báo"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    # Tính thời gian gửi warning tiếp theo (6h sáng)
    next_warning = now.replace(hour=6, minute=0, second=0, microsecond=0)
    if now.hour >= 6:
        next_warning += timedelta(days=1)
    
    # Tính thời gian xóa tiếp theo (2h51 sáng)
    next_delete = now.replace(hour=2, minute=51, second=0, microsecond=0)
    if now.hour >= 3:
        next_delete += timedelta(days=1)
    
    # Đếm số thành viên có role Warning
    guild = interaction.guild
    role = guild.get_role(WARNING_ROLE_ID)
    warning_count = len([member for member in guild.members if role in member.roles]) if role else 0
    
    status_content = f"""
� **TRẠNGt THÁI HỆ THỐNG NHẮC NHỞ**

⏰ **Thời gian hiện tại**: {now.strftime('%H:%M:%S %d/%m/%Y')}

� **Ghửi nhắc nhở tiếp theo**: {next_warning.strftime('%H:%M %d/%m/%Y')}
🗑️ **Xóa tin nhắn tiếp theo**: {next_delete.strftime('%H:%M %d/%m/%Y')}

� **Cấu hình:**
🎭 **Role ID**: {WARNING_ROLE_ID}
📺 **Channel ID**: {WARNING_CHANNEL_ID}

👥 **Thành viên Warning hiện tại**: {warning_count}
📊 **Tin nhắn đang theo dõi**: {len(bot.warning_messages)}

💡 **Lệnh admin:**
• `/test-warning` - Test gửi nhắc nhở
• `/xoa-warning` - Xóa tất cả tin nhắn
• `/warning-status` - Xem trạng thái này
"""
    
    await interaction.response.send_message(status_content, ephemeral=True)

@bot.tree.command(name="list-warning", description="👥 [ADMIN] Xem danh sách thành viên Warning")
async def list_warning_command(interaction: discord.Interaction):
    """Xem danh sách thành viên có role Warning"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    guild = interaction.guild
    role = guild.get_role(WARNING_ROLE_ID)
    
    if not role:
        await interaction.response.send_message(f"❌ Không tìm thấy role Warning (ID: {WARNING_ROLE_ID})!", ephemeral=True)
        return
    
    warning_members = [member for member in guild.members if role in member.roles]
    
    if not warning_members:
        await interaction.response.send_message("📭 Hiện tại không có thành viên nào có role Warning!", ephemeral=True)
        return
    
    # Tạo danh sách thành viên
    member_list = ""
    for i, member in enumerate(warning_members, 1):
        member_list += f"{i}. **{member.display_name}** ({member.mention})\n"
        
        # Giới hạn 20 thành viên để tránh tin nhắn quá dài
        if i >= 20:
            member_list += f"... và {len(warning_members) - 20} thành viên khác\n"
            break
    
    list_content = f"""
👥 **DANH SÁCH THÀNH VIÊN WARNING**

🎭 **Role**: {role.name} ({role.id})
👤 **Tổng số**: {len(warning_members)} thành viên

📋 **Danh sách:**
{member_list}

💡 **Lưu ý**: Những thành viên này sẽ nhận nhắc nhở lúc 6h sáng hàng ngày.
"""
    
    await interaction.response.send_message(list_content, ephemeral=True)

# ==================== PENDINGKICK SYSTEM COMMANDS ====================

@bot.tree.command(name="debug-tasks", description="🔧 [ADMIN] Debug trạng thái scheduled tasks")
async def debug_tasks_command(interaction: discord.Interaction):
    """Debug trạng thái các scheduled tasks"""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Chỉ admin mới có thể dùng lệnh này!", ephemeral=True)
        return
    
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    
    # Kiểm tra trạng thái tasks
    daily_status = "✅ Running" if bot.auto_post_daily_task and not bot.auto_post_daily_task.done() else "❌ Stopped"
    weekly_status = "✅ Running" if bot.auto_post_weekly_task and not bot.auto_post_weekly_task.done() else "❌ Stopped"
    monthly_status = "✅ Running" if bot.auto_post_monthly_task and not bot.auto_post_monthly_task.done() else "❌ Stopped"
    countdown_status = "✅ Running" if bot.countdown_update_task and not bot.countdown_update_task.done() else "❌ Stopped"
    warning_status = "✅ Running" if bot.warning_task and not bot.warning_task.done() else "❌ Stopped"
    pendingkick_status = "✅ Running" if bot.pendingkick_task and not bot.pendingkick_task.done() else "❌ Stopped"
    
    # Tính thời gian gửi tiếp theo
    next_daily = now.replace(hour=2, minute=58, second=0, microsecond=0)
    if now.hour >= 3:
        next_daily += timedelta(days=1)
    
    next_weekly_8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    next_weekly_3am = now.replace(hour=2, minute=55, second=0, microsecond=0)
    if now.hour >= 20:
        next_weekly_8pm += timedelta(days=1)
    if now.hour >= 3:
        next_weekly_3am += timedelta(days=1)
    
    next_monthly = None
    for day in [1, 15]:
        candidate = now.replace(day=day, hour=2, minute=50, second=0, microsecond=0)
        if candidate > now:
            next_monthly = candidate
            break
    if not next_monthly:
        # Next month
        if now.month == 12:
            next_monthly = now.replace(year=now.year+1, month=1, day=1, hour=2, minute=50, second=0, microsecond=0)
        else:
            next_monthly = now.replace(month=now.month+1, day=1, hour=2, minute=50, second=0, microsecond=0)
    
    debug_content = f"""
🔧 **DEBUG SCHEDULED TASKS**

⏰ **Thời gian hiện tại**: {now.strftime('%H:%M:%S %d/%m/%Y')}

📊 **Trạng thái Tasks:**
• **Daily Task**: {daily_status}
• **Weekly Task**: {weekly_status}
• **Monthly Task**: {monthly_status}
• **Countdown Task**: {countdown_status}
• **Warning Task**: {warning_status}
• **PendingKick Task**: {pendingkick_status}

⏰ **Lịch gửi tiếp theo:**
• **Daily**: {next_daily.strftime('%H:%M %d/%m/%Y')}
• **Weekly (8PM)**: {next_weekly_8pm.strftime('%H:%M %d/%m/%Y')}
• **Weekly (3AM)**: {next_weekly_3am.strftime('%H:%M %d/%m/%Y')}
• **Monthly**: {next_monthly.strftime('%H:%M %d/%m/%Y')}

📋 **Channel IDs:**
• **Daily**: {CHANNEL_DAILY}
• **Weekly**: {CHANNEL_WEEKLY}
• **Monthly**: {CHANNEL_MONTHLY}

💡 **Nếu task bị stopped, restart bot để khởi động lại.**
"""
    
    await interaction.response.send_message(debug_content, ephemeral=True)

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

async def wakeup_command(interaction: discord.Interaction, target_type: str, target_user: discord.Member = None):
    """Hệ thống đánh thức học tập thông minh"""
    
    # Kiểm tra cooldown để tránh spam
    user_id = interaction.user.id
    now = time.time()
    
    if user_id in bot.wakeup_cooldown:
        time_left = bot.wakeup_cooldown[user_id] + bot.wakeup_cooldown_duration - now
        if time_left > 0:
            minutes = int(time_left // 60)
            seconds = int(time_left % 60)
            await interaction.response.send_message(
                f"⏰ Bạn cần đợi {minutes}m {seconds}s nữa mới có thể đánh thức tiếp!", 
                ephemeral=True
            )
            return
    
    # Cập nhật cooldown
    bot.wakeup_cooldown[user_id] = now
    
    # Respond ngay để tránh timeout
    await interaction.response.send_message("🔔 Đang chuẩn bị đánh thức...", ephemeral=True)
    
    try:
        # Tạo nội dung đánh thức
        wakeup_content = await generate_wakeup_content(interaction.user, target_type, target_user)
        
        if target_type == "channel":
            # Gửi vào kênh đánh thức
            wakeup_channel = bot.get_channel(WAKEUP_CHANNEL)
            if wakeup_channel:
                await wakeup_channel.send(wakeup_content)
                await interaction.followup.send(f"✅ Đã gửi đánh thức vào <#{WAKEUP_CHANNEL}>!", ephemeral=True)
            else:
                await interaction.followup.send("❌ Không tìm thấy kênh đánh thức!", ephemeral=True)
        else:
            # Gửi trong channel hiện tại
            await interaction.channel.send(wakeup_content)
            await interaction.followup.send("✅ Đã gửi đánh thức!", ephemeral=True)
            
        print(f"🔔 {interaction.user.name} đã đánh thức ({target_type})")
        
    except Exception as e:
        print(f"❌ Lỗi đánh thức: {e}")
        await interaction.followup.send("❌ Có lỗi xảy ra khi đánh thức!", ephemeral=True)

async def generate_wakeup_content(caller: discord.Member, target_type: str, target_user: discord.Member = None):
    """Tạo nội dung đánh thức thông minh và thú vị"""
    
    # Lấy thời gian hiện tại
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(vn_tz)
    time_str = now.strftime("%H:%M")
    
    # Emoji và âm thanh đánh thức
    wakeup_emojis = ["🔔", "⏰", "📢", "🎺", "🔊", "⚡", "💪", "🚀", "🎯", "📚"]
    motivational_emojis = ["💪", "🔥", "⭐", "🏆", "🎯", "📈", "💎", "🚀", "⚡", "🌟"]
    
    # Random emoji cho mỗi lần đánh thức
    import random
    wake_emoji = random.choice(wakeup_emojis)
    moti_emoji = random.choice(motivational_emojis)
    
    # Câu động viên ngẫu nhiên
    motivational_quotes = [
        "Thành công bắt đầu từ việc thức dậy sớm!",
        "Mỗi phút trôi qua là một cơ hội học tập!",
        "Hôm nay bạn sẽ học được điều gì mới?",
        "Kiến thức là sức mạnh, hãy tích lũy ngay!",
        "Đừng để thời gian trôi qua vô ích!",
        "Học tập là đầu tư tốt nhất cho tương lai!",
        "Mỗi ngày học một chút, thành công sẽ đến!",
        "Hãy biến giấc mơ thành hiện thực!",
        "Chỉ có học tập mới thay đổi cuộc đời!",
        "Bắt đầu ngay bây giờ, đừng chờ đợi!"
    ]
    
    quote = random.choice(motivational_quotes)
    
    # Tạo nội dung dựa trên loại đánh thức
    if target_type == "all":
        content = f"""
{wake_emoji} **ĐÁNH THỨC HỌC TẬP** {wake_emoji}

@everyone 

{moti_emoji} **{quote}** {moti_emoji}

🕐 **Thời gian**: {time_str}
👤 **Người đánh thức**: {caller.mention}
📚 **Thông điệp**: Đã đến lúc học tập rồi! Hãy cùng nhau nỗ lực nhé!

**🎯 Hãy bắt đầu học ngay:**
• Mở sách/laptop
• Tập trung 100%
• Tắt điện thoại
• Uống nước, ngồi thẳng

**⏰ Pomodoro Suggestion:**
25 phút học → 5 phút nghỉ → Lặp lại

{moti_emoji} *Cùng nhau tiến bộ mỗi ngày!* {moti_emoji}
"""
    
    elif target_type == "user" and target_user:
        # Kiểm tra xem user có đang online không
        status_emoji = "🟢" if target_user.status == discord.Status.online else "🔴"
        
        content = f"""
{wake_emoji} **ĐÁNH THỨC CÁ NHÂN** {wake_emoji}

{target_user.mention} {status_emoji}

{moti_emoji} **{quote}** {moti_emoji}

🕐 **Thời gian**: {time_str}
👤 **Người đánh thức**: {caller.mention}
🎯 **Mục tiêu**: Đã đến lúc {target_user.display_name} học tập rồi!

**📋 Checklist cho bạn:**
✅ Chuẩn bị tài liệu
✅ Tìm chỗ ngồi thoải mái  
✅ Đặt mục tiêu cụ thể
✅ Bắt đầu ngay!

{moti_emoji} *Bạn làm được mà! Fighting!* {moti_emoji}
"""
    
    elif target_type == "channel":
        # Đánh thức đặc biệt cho kênh đánh thức
        content = f"""
{wake_emoji}🎺 **TIẾNG KÈNG HỌC TẬP** 🎺{wake_emoji}

@everyone 

🔥 **EMERGENCY STUDY ALERT** 🔥

{moti_emoji} **{quote}** {moti_emoji}

🕐 **Thời gian báo động**: {time_str}
👤 **Chỉ huy trưởng**: {caller.mention}
📍 **Địa điểm tập trung**: Bàn học của bạn!

**🚨 LỆNH KHẨN CẤP:**
1. 🏃‍♂️ Chạy đến bàn học NGAY
2. 📚 Mở sách/laptop trong 30 giây
3. 🎯 Đặt mục tiêu học trong 1 phút
4. ⏰ Bắt đầu học trong 2 phút

**🏆 PHẦN THƯỞNG:**
• Kiến thức mới
• Cảm giác thành tựu
• Tương lai tươi sáng

{moti_emoji} **AI KHÔNG HỌC BÂY GIỜ THÌ KHI NÀO?** {moti_emoji}

*Tin nhắn này sẽ tự hủy sau khi bạn bắt đầu học... 😄*
"""
    
    return content

def generate_countdown_name(base_name: str, time_left: timedelta, format_type: str) -> str:
    """Tạo tên phòng đếm ngược với nhiều định dạng"""
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if format_type == "countdown_compact":
        # Chỉ hiển thị đếm ngược compact: "125d22h30p"
        return f"{days}d{hours:02d}h{minutes:02d}p"
    
    elif format_type == "countdown_verbose":
        # Chỉ hiển thị đếm ngược verbose: "125 ngày 22 giờ 30 phút"
        return f"{days} ngày {hours} giờ {minutes} phút"
    
    elif format_type == "full_compact":
        # Tên + đếm ngược compact: "JLPT Còn 125d22h30p"
        return f"{base_name} Còn {days}d{hours:02d}h{minutes:02d}p"
    
    elif format_type == "full_verbose":
        # Tên + đếm ngược verbose: "JLPT Còn 125 ngày 22 giờ 30 phút"
        return f"{base_name} Còn {days} ngày {hours} giờ {minutes} phút"
    
    else:
        # Fallback về full_compact nếu format không hợp lệ
        return f"{base_name} Còn {days}d{hours:02d}h{minutes:02d}p"

def parse_date_string(date_str: str) -> datetime:
    """Parse chuỗi ngày tháng thành datetime"""
    # Hỗ trợ các format: DD/MM/YYYY, D/M/YYYY, DD/MM/YY
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    
    # Thử các format khác nhau
    formats = [
        "%d/%m/%Y",    # 09/12/2025
        "%d/%m/%y",    # 09/12/25
        "%-d/%-m/%Y",  # 9/12/2025 (Unix)
        "%#d/%#m/%Y"   # 9/12/2025 (Windows)
    ]
    
    for fmt in formats:
        try:
            # Parse ngày
            parsed_date = datetime.strptime(date_str, fmt)
            
            # Nếu năm < 100, coi như 20xx
            if parsed_date.year < 100:
                parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
            
            # Set thời gian là 23:59:59 của ngày đó
            parsed_date = parsed_date.replace(hour=23, minute=59, second=59)
            
            # Thêm timezone
            return vn_tz.localize(parsed_date)
            
        except ValueError:
            continue
    
    # Nếu không parse được, thử format đơn giản
    try:
        parts = date_str.split('/')
        if len(parts) == 3:
            day, month, year = map(int, parts)
            
            # Xử lý năm 2 chữ số
            if year < 100:
                year += 2000
            
            parsed_date = datetime(year, month, day, 23, 59, 59)
            return vn_tz.localize(parsed_date)
    except:
        pass
    
    raise ValueError(f"Không thể parse ngày: {date_str}")

async def create_countdown_room(interaction: discord.Interaction, name: str, date_str: str, format_type: str):
    """Tạo phòng học đếm ngược"""
    try:
        # Validate format_type
        valid_formats = ["full_verbose", "full_compact", "countdown_verbose", "countdown_compact"]
        if format_type not in valid_formats:
            await interaction.response.send_message(
                f"❌ Format không hợp lệ!\n"
                f"**Hỗ trợ:** {', '.join(valid_formats)}", 
                ephemeral=True
            )
            return
        
        # Parse ngày
        try:
            target_date = parse_date_string(date_str)
        except ValueError as e:
            await interaction.response.send_message(
                f"❌ Định dạng ngày không hợp lệ!\n"
                f"**Hỗ trợ:** DD/MM/YYYY hoặc D/M/YYYY\n"
                f"**Ví dụ:** 9/12/2025, 09/12/2025\n"
                f"**Lỗi:** {e}", 
                ephemeral=True
            )
            return
        
        # Kiểm tra ngày có trong tương lai không
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vn_tz)
        
        if target_date <= now:
            await interaction.response.send_message("❌ Ngày mục tiêu phải trong tương lai!", ephemeral=True)
            return
        
        # Kiểm tra user đã có phòng chưa
        user_rooms = [room for room in bot.countdown_rooms.values() if room['creator_id'] == interaction.user.id]
        if len(user_rooms) >= 3:  # Giới hạn 3 phòng/user
            await interaction.response.send_message("❌ Bạn chỉ có thể tạo tối đa 3 phòng đếm ngược!", ephemeral=True)
            return
        
        await interaction.response.send_message("🏗️ Đang tạo phòng học đếm ngược...", ephemeral=True)
        
        # Tính toán tên phòng ban đầu
        time_left = target_date - now
        initial_name = generate_countdown_name(name, time_left, format_type)
        
        # Lấy category
        category = bot.get_channel(STUDY_ROOMS_CATEGORY)
        if not category:
            await interaction.followup.send("❌ Không tìm thấy danh mục phòng học!", ephemeral=True)
            return
        
        # Tạo overwrites (quyền)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=True,      # Mọi người xem được
                connect=False,          # Nhưng không kết nối được
                send_messages=False     # Không gửi tin nhắn được
            ),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                connect=True,           # Creator có thể kết nối
                manage_channels=True,   # Creator có thể quản lý phòng
                send_messages=True,     # Creator có thể gửi tin nhắn
                manage_messages=True    # Creator có thể quản lý tin nhắn
            )
        }
        
        # Tạo voice channel
        voice_channel = await category.create_voice_channel(
            name=initial_name,
            overwrites=overwrites,
            reason=f"Countdown room created by {interaction.user}"
        )
        
        # Lưu thông tin phòng
        bot.countdown_rooms[voice_channel.id] = {
            'name': name,
            'target_date': target_date,
            'creator_id': interaction.user.id,
            'format_type': format_type
        }
        
        # Tạo thông báo thành công
        format_descriptions = {
            "full_verbose": "Tên + Còn xx ngày xx giờ xx phút",
            "full_compact": "Tên + Còn xxdxxhxxp", 
            "countdown_verbose": "xx ngày xx giờ xx phút",
            "countdown_compact": "xxdxxhxxp"
        }
        
        success_message = f"""
✅ **PHÒNG HỌC ĐÃ TẠO THÀNH CÔNG!**

📚 **Tên phòng**: {initial_name}
🎯 **Mục tiêu**: {target_date.strftime('%d/%m/%Y %H:%M')}
⏰ **Thời gian còn lại**: {time_left.days} ngày {time_left.seconds//3600} giờ
👤 **Chủ phòng**: {interaction.user.mention}
🎨 **Định dạng**: {format_descriptions.get(format_type, format_type)}

**🔧 Quyền của bạn:**
• ✅ Kết nối vào phòng
• ✅ Quản lý phòng (đổi tên, xóa)
• ✅ Gửi tin nhắn trong phòng

**📋 Lưu ý:**
• Tên phòng tự động cập nhật mỗi 5 phút
• Phòng tự động xóa khi hết thời gian
• Mọi người có thể xem nhưng không kết nối được
• Dùng `/xoa-phong-hoc` để xóa phòng

🎉 **Chúc bạn học tập hiệu quả!**
"""
        
        await interaction.followup.send(success_message, ephemeral=True)
        
        print(f"✅ Tạo phòng đếm ngược: {initial_name} (Creator: {interaction.user.name})")
        
    except Exception as e:
        print(f"❌ Lỗi tạo phòng đếm ngược: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            await interaction.followup.send("❌ Có lỗi xảy ra khi tạo phòng!", ephemeral=True)
        except:
            pass

async def delete_countdown_room(interaction: discord.Interaction):
    """Xóa phòng học đếm ngược của user"""
    try:
        # Tìm phòng của user
        user_rooms = []
        for channel_id, room_info in bot.countdown_rooms.items():
            if room_info['creator_id'] == interaction.user.id:
                channel = bot.get_channel(channel_id)
                if channel:
                    user_rooms.append((channel_id, channel, room_info))
        
        if not user_rooms:
            await interaction.response.send_message("❌ Bạn không có phòng đếm ngược nào!", ephemeral=True)
            return
        
        if len(user_rooms) == 1:
            # Chỉ có 1 phòng - xóa luôn
            channel_id, channel, room_info = user_rooms[0]
            
            await interaction.response.send_message(f"🗑️ Đang xóa phòng '{channel.name}'...", ephemeral=True)
            
            try:
                await channel.delete(reason=f"Deleted by creator {interaction.user}")
                del bot.countdown_rooms[channel_id]
                
                await interaction.followup.send(f"✅ Đã xóa phòng '{room_info['name']}'!", ephemeral=True)
                print(f"🗑️ Xóa phòng đếm ngược: {room_info['name']} (Creator: {interaction.user.name})")
                
            except Exception as e:
                await interaction.followup.send(f"❌ Lỗi xóa phòng: {e}", ephemeral=True)
        
        else:
            # Có nhiều phòng - hiển thị danh sách
            room_list = ""
            for i, (channel_id, channel, room_info) in enumerate(user_rooms, 1):
                vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                now = datetime.now(vn_tz)
                time_left = room_info['target_date'] - now
                
                room_list += f"{i}. **{room_info['name']}** - Còn {time_left.days}d{time_left.seconds//3600:02d}h\n"
            
            message = f"""
📋 **DANH SÁCH PHÒNG CỦA BẠN**

{room_list}

⚠️ **Để xóa phòng cụ thể:**
1. Vào phòng đó và dùng lệnh `/xoa-phong-hoc`
2. Hoặc xóa trực tiếp trong Discord (chuột phải > Delete Channel)

💡 **Mẹo**: Bạn có thể quản lý phòng trực tiếp trong Discord!
"""
            
            await interaction.response.send_message(message, ephemeral=True)
            
    except Exception as e:
        print(f"❌ Lỗi xóa phòng đếm ngược: {e}")
        await interaction.response.send_message("❌ Có lỗi xảy ra!", ephemeral=True)

async def list_countdown_rooms(interaction: discord.Interaction):
    """Hiển thị danh sách phòng đếm ngược"""
    try:
        if not bot.countdown_rooms:
            await interaction.response.send_message("📭 Hiện tại không có phòng đếm ngược nào!", ephemeral=True)
            return
        
        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(vn_tz)
        
        room_list = ""
        user_rooms = ""
        
        for channel_id, room_info in bot.countdown_rooms.items():
            channel = bot.get_channel(channel_id)
            if not channel:
                continue
            
            time_left = room_info['target_date'] - now
            creator = bot.get_user(room_info['creator_id'])
            creator_name = creator.display_name if creator else "Unknown"
            
            room_entry = f"📚 **{room_info['name']}** - Còn {time_left.days}d{time_left.seconds//3600:02d}h{(time_left.seconds%3600)//60:02d}p\n"
            room_entry += f"   👤 {creator_name} | 🎯 {room_info['target_date'].strftime('%d/%m/%Y')}\n\n"
            
            if room_info['creator_id'] == interaction.user.id:
                user_rooms += room_entry
            else:
                room_list += room_entry
        
        message = "📋 **DANH SÁCH PHÒNG HỌC ĐẾMNGƯỢC**\n\n"
        
        if user_rooms:
            message += "🏠 **PHÒNG CỦA BẠN:**\n" + user_rooms
        
        if room_list:
            message += "🌍 **PHÒNG CỦA THÀNH VIÊN KHÁC:**\n" + room_list
        
        message += "💡 **Mẹo**: Dùng `/tao-phong-hoc` để tạo phòng mới!"
        
        await interaction.response.send_message(message, ephemeral=True)
        
    except Exception as e:
        print(f"❌ Lỗi hiển thị danh sách phòng: {e}")
        await interaction.response.send_message("❌ Có lỗi xảy ra!", ephemeral=True)

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