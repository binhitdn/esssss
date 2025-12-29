# StudyLion Leaderboard Bot

Bot Discord hiển thị bảng xếp hạng học tập với GUI đẹp mắt, lấy dữ liệu từ API thật.

## 🎯 Tính năng

- **3 loại bảng xếp hạng**: Ngày, Tuần, Tháng
- **GUI đẹp mắt**: Sử dụng GUI system của LionBot gốc
- **Dữ liệu thật**: Lấy từ API với avatar và thời gian thực
- **Múi giờ Việt Nam**: Hiển thị thời gian theo UTC+7
- **Loại bỏ emoji**: Tự động làm sạch tên người dùng
- **Chỉ 1 server**: Bảo mật cho server riêng
- **Tự động gửi bảng xếp hạng**:
  - 📅 **Ngày**: Mỗi ngày lúc 2h58 sáng
  - 📅 **Tuần**: Mỗi ngày lúc 20h và 2h55 sáng
  - 📅 **Tháng**: Ngày 1 và 15 mỗi tháng lúc 2h50 sáng

## 📋 Lệnh Discord

### Slash Commands (Thủ công)
- `/bangxephang` - Bảng xếp hạng hôm nay
- `/bangxephang-tuan` - Bảng xếp hạng tuần này  
- `/bangxephang-thang` - Bảng xếp hạng tháng này

### Tự động gửi
Bot sẽ tự động gửi bảng xếp hạng theo lịch:

| Loại | Thời gian | Channel ID |
|------|-----------|------------|
| 📅 Ngày | 2h58 sáng mỗi ngày | 1450690801934930124 |
| 📅 Tuần | 20h và 2h55 mỗi ngày | 1435035898629591040 |
| 📅 Tháng | Ngày 1 & 15 lúc 2h50 | 1450690861036994763 |

*Tất cả theo múi giờ Việt Nam (UTC+7)*

## 🚀 Cách chạy

### Phương pháp 1: Script Python (Khuyến nghị)
```bash
python3 start.py
```

### Phương pháp 2: Script Bash
```bash
chmod +x start.sh
./start.sh
```

### Phương pháp 3: Chạy thủ công
```bash
python3 run_leaderboard_bot.py
```

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

### 3. Cấu hình Server ID
Trong `leaderboard_only_bot.py`, sửa:
```python
ALLOWED_SERVER_ID = 1434581250798125068  # Thay bằng server ID của bạn
```

### 4. Cấu hình Channel IDs (Tự động gửi)
Trong `leaderboard_only_bot.py`, sửa:
```python
CHANNEL_DAILY = 1450690801934930124      # Channel cho bảng xếp hạng ngày
CHANNEL_WEEKLY = 1435035898629591040     # Channel cho bảng xếp hạng tuần
CHANNEL_MONTHLY = 1450690861036994763    # Channel cho bảng xếp hạng tháng
```

### 5. Cấu hình API
Trong `leaderboard_only_bot.py`, sửa:
```python
API_BASE_URL = "http://192.168.128.173:3001/api/leaderboard/top-learners"
```

## 📁 Cấu trúc Project

```
StudyLion/
├── start.py                    # Script khởi động Python
├── start.sh                    # Script khởi động Bash  
├── run_leaderboard_bot.py      # Script chạy thủ công
├── leaderboard_only_bot.py     # Bot chính
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