# StudyLion Leaderboard Bot + Web Dashboard

Bot Discord hiển thị bảng xếp hạng học tập với GUI đẹp mắt + Web Dashboard thống kê server, lấy dữ liệu từ API thật.

## 🎯 Tính năng

### Discord Bot
- **3 loại bảng xếp hạng**: Ngày, Tuần, Tháng
- **🔔 Hệ thống đánh thức học tập (MỚI!)**:
  - Đánh thức tất cả (@everyone)
  - Đánh thức user cụ thể
  - Đánh thức vào kênh chuyên dụng
  - Hẹn giờ đánh thức thông minh
  - Timer Pomodoro tự động
  - Thống kê đánh thức cá nhân
- **📚 Hệ thống phòng học đếm ngược (MỚI!)**:
  - Tạo phòng voice đếm ngược đến ngày mục tiêu
  - Tự động cập nhật tên phòng mỗi 5 phút
  - Creator có full quyền, người khác chỉ xem
  - Tự động xóa khi hết thời gian
  - Hỗ trợ 2 định dạng hiển thị
- **⚠️ Hệ thống cảnh báo tự động (MỚI!)**:
  - Tự động gửi cảnh báo lúc 6h sáng
  - Tag user cụ thể với thông tin học tập
  - Tự động xóa tin nhắn lúc 2h51 sáng hôm sau
  - Lệnh admin để quản lý và test
- **🚨 Hệ thống PendingKick tự động (MỚI!)**:
  - Tự động gửi thông báo cho role PendingKick lúc 6h sáng
  - Tag tất cả thành viên có role cụ thể
  - Tự động xóa tin nhắn lúc 2h51 sáng hôm sau
  - Lệnh admin để quản lý và xem danh sách
- **GUI đẹp mắt**: Sử dụng GUI system của LionBot gốc
- **Dữ liệu thật**: Lấy từ API với avatar và thời gian thực
- **Múi giờ Việt Nam**: Hiển thị thời gian theo UTC+7
- **Loại bỏ emoji**: Tự động làm sạch tên người dùng
- **Chỉ 1 server**: Bảo mật cho server riêng
- **Tự động gửi bảng xếp hạng**:
  - 📅 **Ngày**: Mỗi ngày lúc 2h58 sáng
  - 📅 **Tuần**: Mỗi ngày lúc 20h và 2h55 sáng
  - 📅 **Tháng**: Ngày 1 và 15 mỗi tháng lúc 2h50 sáng

### 🌐 Web Dashboard (MỚI!)
- **📊 Server Dashboard**: Thống kê thật từ Discord server (thành viên, roles, channels, voice activity)
- **🏆 Leaderboard Demo**: Bảng xếp hạng demo cho minh họa
- **📈 Advanced Analytics**: Biểu đồ, phân tích xu hướng
- **🔄 Auto refresh**: Tự động cập nhật mỗi 30-60 giây
- **📱 Responsive**: Tương thích mobile và desktop
- **🎨 UI đẹp**: Giao diện hiện đại với gradient và animations

## 📋 Lệnh Discord

### Slash Commands - Bảng Xếp Hạng
- `/bangxephang` - Bảng xếp hạng hôm nay
- `/bangxephang-tuan` - Bảng xếp hạng tuần này  
- `/bangxephang-thang` - Bảng xếp hạng tháng này

### 🔔 Slash Commands - Đánh Thức Học Tập (MỚI!)
- `/danh-thuc` - 🔔 Đánh thức tất cả mọi người (@everyone)
- `/danh-thuc-user @user` - 🎯 Đánh thức một người cụ thể
- `/danh-thuc-kenh` - 📢 Gửi đánh thức vào kênh chuyên dụng (ID: 1456243735938600970)
- `/danh-thuc-hen-gio [phút] [tin nhắn]` - ⏰ Hẹn giờ đánh thức sau X phút
- `/danh-thuc-pomodoro [chu kỳ]` - 🍅 Timer Pomodoro (25p học + 5p nghỉ)
- `/danh-thuc-stats` - 📊 Xem thống kê đánh thức cá nhân

### 📚 Slash Commands - Phòng Học Đếm Ngược (MỚI!)
- `/tao-phong-hoc [tên] [ngày] [định dạng]` - 🏗️ Tạo phòng đếm ngược đến ngày mục tiêu
- `/xoa-phong-hoc` - 🗑️ Xóa phòng học đếm ngược của bạn
- `/danh-sach-phong-hoc` - 📋 Xem tất cả phòng đếm ngược

### ⚠️ Slash Commands - Hệ Thống Cảnh Báo (MỚI!)
- `/test-warning` - 🧪 [ADMIN] Test gửi cảnh báo ngay
- `/xoa-warning` - 🗑️ [ADMIN] Xóa tất cả tin nhắn cảnh báo
- `/warning-status` - 📊 [ADMIN] Xem trạng thái hệ thống cảnh báo

### 🚨 Slash Commands - Hệ Thống PendingKick (MỚI!)
- `/test-pendingkick` - 🧪 [ADMIN] Test gửi PendingKick ngay
- `/xoa-pendingkick` - 🗑️ [ADMIN] Xóa tất cả tin nhắn PendingKick
- `/pendingkick-status` - 📊 [ADMIN] Xem trạng thái hệ thống PendingKick
- `/list-pendingkick` - 👥 [ADMIN] Xem danh sách thành viên PendingKick

**Tính năng đặc biệt:**
- ⏰ **Cooldown 5 phút**: Tránh spam đánh thức
- 🎲 **Nội dung ngẫu nhiên**: Mỗi lần đánh thức có câu động viên khác nhau
- 🍅 **Pomodoro Timer**: Tự động báo học 25p và nghỉ 5p
- 📊 **Thống kê cá nhân**: Theo dõi số lần đánh thức và streak
- 🏠 **Phòng riêng**: Creator có full quyền, người khác chỉ xem
- ⏰ **Tự động cập nhật**: Tên phòng cập nhật mỗi 5 phút
- 🗑️ **Tự động xóa**: Phòng tự xóa khi hết thời gian

### Tự động gửi
Bot sẽ tự động gửi bảng xếp hạng theo lịch:

| Loại | Thời gian | Channel ID |
|------|-----------|------------|
| 📅 Ngày | 2h58 sáng mỗi ngày | 1450690801934930124 |
| 📅 Tuần | 20h và 2h55 mỗi ngày | 1435035898629591040 |
| 📅 Tháng | Ngày 1 & 15 lúc 2h50 | 1450690861036994763 |

*Tất cả theo múi giờ Việt Nam (UTC+7)*

## 🚀 Cách chạy

### Phương pháp 1: Full System (Bot + GUI + Web) - Khuyến nghị
```bash
python3 start_with_web.py
```
**Bao gồm:**
- Discord Bot với GUI
- Web Dashboard tại http://localhost:5001
- **🔔 Hệ thống đánh thức học tập**
- Tất cả tính năng

### Phương pháp 2: Chỉ Bot + GUI
```bash
python3 start.py
```

### Phương pháp 3: Chỉ Web Dashboard (Dữ liệu Discord)
```bash
python3 run_web_only.py
```

### Phương pháp 4: Script Bash (Bot only)
```bash
chmod +x start.sh
./start.sh
```

## 🔔 Hướng Dẫn Sử Dụng Đánh Thức

### Lệnh Cơ Bản
```
/danh-thuc                    # Đánh thức tất cả (@everyone)
/danh-thuc-user @username     # Đánh thức một người
/danh-thuc-kenh              # Gửi vào kênh đánh thức
```

### Lệnh Nâng Cao
```
/danh-thuc-hen-gio 30 "Làm bài tập"    # Hẹn giờ 30 phút
/danh-thuc-pomodoro 3                   # 3 chu kỳ Pomodoro
/danh-thuc-stats                        # Xem thống kê cá nhân
```

### Lệnh Phòng Học Đếm Ngược
```
/tao-phong-hoc "JLPT" "9/12/2025" "full"     # Tạo phòng "JLPT Còn 125d22h23p"
/tao-phong-hoc "Thi cuối kỳ" "15/1/2026" "countdown"  # Tạo phòng "89d15h42p"
/danh-sach-phong-hoc                          # Xem tất cả phòng
/xoa-phong-hoc                               # Xóa phòng của bạn
```

### Lệnh Admin (Cảnh Báo)
```
/test-warning                    # Test gửi cảnh báo ngay
/xoa-warning                     # Xóa tất cả tin nhắn cảnh báo  
/warning-status                  # Xem trạng thái hệ thống
```

### Lệnh Admin (PendingKick)
```
/test-pendingkick               # Test gửi PendingKick ngay
/xoa-pendingkick                # Xóa tất cả tin nhắn PendingKick
/pendingkick-status             # Xem trạng thái hệ thống
/list-pendingkick               # Xem danh sách thành viên PendingKick
```

### Mẹo Sử Dụng
- **Cooldown**: 5 phút/người để tránh spam
- **Thời điểm tốt**: 6h-8h, 13h-14h, 19h-21h
- **Pomodoro**: Bắt đầu với 1-2 chu kỳ, tăng dần
- **Hẹn giờ**: Tối đa 24 giờ (1440 phút)
- **Phòng đếm ngược**: Tối đa 3 phòng/người
- **Định dạng ngày**: DD/MM/YYYY hoặc D/M/YYYY
- **Quyền phòng**: Creator quản lý, người khác chỉ xem
- **Cảnh báo tự động**: 6h sáng gửi, 2h51 sáng xóa
- **PendingKick tự động**: 6h sáng gửi cho role, 2h51 sáng xóa
- **Lệnh admin**: Chỉ admin mới dùng được lệnh warning/pendingkick

## ⚙️ Cấu hình

### 1. Tạo Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Cấu hình Bot Token
Tạo file `config/secrets.conf`:
```ini
[STUDYLION]
token = YOUR_BOT_TOKEN_HERE
```

### 3. Sync Slash Commands (Quan trọng!)
**Lần đầu chạy hoặc khi thêm lệnh mới:**
```bash
python3 sync_commands.py
python3 start.py
```

**Hoặc tạo file thủ công:**
```bash
touch .sync_commands
python3 start.py
```

Bot sẽ tự động sync và xóa file `.sync_commands` sau khi hoàn tất.

### 4. Cấu hình Server ID
Trong `leaderboard_only_bot.py`, sửa:
```python
ALLOWED_SERVER_ID = 1434581250798125068  # Thay bằng server ID của bạn
```

### 5. Cấu hình Channel IDs
Trong `leaderboard_only_bot.py`, sửa:
```python
CHANNEL_DAILY = 1450690801934930124      # Channel cho bảng xếp hạng ngày
CHANNEL_WEEKLY = 1435035898629591040     # Channel cho bảng xếp hạng tuần
CHANNEL_MONTHLY = 1450690861036994763    # Channel cho bảng xếp hạng tháng
WAKEUP_CHANNEL = 1456243735938600970     # Channel đánh thức học tập
STUDY_ROOMS_CATEGORY = 1436215086694924449  # Danh mục phòng học đếm ngược
WARNING_USER_ID = 1436409040036040886        # User ID cần tag warning
WARNING_CHANNEL_ID = 1446655389860106361     # Channel gửi warning
PENDINGKICK_ROLE_ID = 1436802180429385768    # Role ID PendingKick
PENDINGKICK_CHANNEL_ID = 1446655276962021497 # Channel gửi PendingKick
```

### 6. Cấu hình API
Trong `leaderboard_only_bot.py`, sửa:
```python
API_BASE_URL = "http://192.168.128.173:3001/api/leaderboard/top-learners"
```

## 📁 Cấu trúc Project

```
StudyLion/
├── start_with_web.py           # Script khởi động Full System (Bot + Web)
├── start.py                    # Script khởi động Bot + GUI
├── start.sh                    # Script khởi động Bash  
├── run_leaderboard_bot.py      # Script chạy thủ công
├── leaderboard_only_bot.py     # Bot chính
├── web/                        # 🌐 Web Dashboard
│   ├── app.py                 # Flask web server
│   ├── start_web.py           # Script khởi động web riêng
│   ├── requirements.txt       # Dependencies cho web
│   ├── templates/
│   │   ├── dashboard.html     # Trang dashboard chính
│   │   └── advanced.html      # Trang analytics nâng cao
│   ├── static/
│   │   └── style.css         # CSS tùy chỉnh
│   └── README.md             # Hướng dẫn web dashboard
├── config/
│   ├── secrets.conf           # Token bot
│   ├── bot.conf              # Cấu hình bot
│   ├── gui.conf              # Cấu hình GUI
│   └── locale.conf           # Cấu hình ngôn ngữ
├── scripts/
│   └── start_gui.py          # GUI server
├── src/gui/                   # GUI system
├── skins/                     # Giao diện bảng xếp hạng
├── locales/vi/               # Ngôn ngữ tiếng Việt
└── venv/                     # Virtual environment
```

## 🔧 API Format

Bot expect API trả về format:
```json
{
  "type": "day|week|month",
  "leaderboard": [
    {
      "rank": 1,
      "userId": "1031850874999423016",
      "userName": "irina",
      "avatar": "1761749d4ee7beee5a19a1669a67cf77",
      "studyTime": 24480755,
      "timeFormatted": {
        "hours": 6,
        "minutes": 48,
        "total": 24480755
      }
    }
  ]
}
```

**Lưu ý**: `studyTime` phải là **milliseconds**, bot sẽ tự chuyển sang giây.

## 🛠️ Troubleshooting

### Bot không khởi động
1. Kiểm tra token trong `config/secrets.conf`
2. Kiểm tra virtual environment: `source venv/bin/activate`
3. Cài đặt dependencies: `pip install -r requirements.txt`

### GUI không render
1. Kiểm tra GUI server có chạy: `ls -la gui.sock`
2. Restart toàn bộ: `python3 start.py`

### API không kết nối
1. Kiểm tra API URL trong code
2. Test API: `curl "http://192.168.128.173:3001/api/leaderboard/top-learners?type=day"`

### Slash commands không sync
1. Kick và invite lại bot vào server
2. Đợi 1-2 phút để Discord sync
3. Restart Discord client

### Tự động gửi không hoạt động
1. Kiểm tra bot có quyền gửi tin nhắn trong channel
2. Kiểm tra Channel IDs có đúng không
3. Xem log khi đến giờ gửi: `⏰ [AUTO] Đang gửi bảng xếp hạng...`
4. Kiểm tra múi giờ server: `date` (phải là UTC+7 hoặc bot tự xử lý)

## 📊 Thống kê

- **Dung lượng**: ~50MB (bao gồm GUI assets)
- **RAM sử dụng**: ~100MB
- **Thời gian khởi động**: ~5 giây
- **Hỗ trợ**: Python 3.9+
- **Tính năng tự động**: 3 scheduled tasks chạy 24/7

## 📚 Tài liệu thêm

- [AUTO_SCHEDULE.md](AUTO_SCHEDULE.md) - Chi tiết về lịch tự động gửi bảng xếp hạng

## 🎨 Tùy chỉnh

### Thay đổi lịch tự động gửi
Sửa trong `leaderboard_only_bot.py`:

**Bảng xếp hạng ngày:**
```python
@tasks.loop(time=time(hour=2, minute=58, tzinfo=VN_TZ))
async def auto_post_daily(self):
    # Thay đổi hour và minute theo ý muốn
```

**Bảng xếp hạng tuần:**
```python
# Trong hàm auto_post_weekly, sửa điều kiện:
if (current_hour == 20 and current_minute == 0) or (current_hour == 2 and current_minute == 55):
    # Thay đổi giờ theo ý muốn
```

**Bảng xếp hạng tháng:**
```python
# Trong hàm auto_post_monthly, sửa điều kiện:
if (now.day == 1 or now.day == 15) and now.hour == 2 and now.minute == 50:
    # Thay đổi ngày và giờ theo ý muốn
```

### Thay đổi màu sắc
Sửa file `src/gui/cards/leaderboard.py`:
```python
top_name_colour: ColourField = '#DDB21D'  # Màu vàng
```

### Thay đổi server name
Sửa trong `leaderboard_only_bot.py`:
```python
'server_name': '14 hours a day(STUDY VIP)'
```

### Thay đổi định dạng thời gian
Sửa trong `src/gui/cards/leaderboard.py`:
```python
study_top_hours_text: LazyStringField = "{HH:02d}:{MM:02d}:{SS:02d}"
```

## 🧪 Test tính năng tự động

### Cách 1: Đợi đến giờ thật
Bot sẽ tự động gửi khi đến giờ đã cấu hình. Xem log:
```
⏰ [AUTO] Đang gửi bảng xếp hạng ngày...
✅ [AUTO] Đã gửi bảng xếp hạng ngày
```

### Cách 2: Test ngay lập tức (Sửa code tạm thời)
Thay đổi thời gian trong code để test:

```python
# Ví dụ: Test bảng xếp hạng ngày sau 1 phút
@tasks.loop(time=time(hour=14, minute=30, tzinfo=VN_TZ))  # Thay bằng giờ hiện tại + 1 phút
async def auto_post_daily(self):
    ...
```

Sau khi test xong, nhớ đổi lại thời gian gốc!

### Cách 3: Gọi hàm trực tiếp (Thêm test command)
Thêm vào `leaderboard_only_bot.py`:

```python
@bot.tree.command(name="test-auto", description="[ADMIN] Test tự động gửi bảng xếp hạng")
async def test_auto_command(interaction: discord.Interaction):
    """Test command cho admin"""
    if interaction.user.id != YOUR_ADMIN_ID:  # Thay bằng Discord ID của bạn
        await interaction.response.send_message("❌ Chỉ admin mới dùng được!", ephemeral=True)
        return
    
    await interaction.response.send_message("🧪 Đang test tự động gửi...", ephemeral=True)
    
    # Test gửi vào channel ngày
    channel = bot.get_channel(CHANNEL_DAILY)
    if channel:
        await bot.send_leaderboard_to_channel(channel, "day", "hôm nay")
        await interaction.followup.send("✅ Đã test gửi bảng xếp hạng ngày!", ephemeral=True)
```

## 📝 License

Private project - Chỉ sử dụng nội bộ.

## 🤝 Support

Nếu có vấn đề, hãy kiểm tra:
1. Log của bot khi chạy
2. API có hoạt động không
3. Token bot có đúng không
4. Server ID có đúng không