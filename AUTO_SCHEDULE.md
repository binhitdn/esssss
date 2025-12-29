# 📅 Lịch Tự Động Gửi Bảng Xếp Hạng

Bot sẽ tự động gửi bảng xếp hạng theo lịch dưới đây (múi giờ Việt Nam - UTC+7):

## 📊 Lịch Gửi

### 🌅 Bảng Xếp Hạng Ngày
- **Thời gian**: 2h58 sáng mỗi ngày
- **Channel**: 1450690801934930124
- **Nội dung**: Top 10 người học chăm chỉ nhất hôm qua

### 📆 Bảng Xếp Hạng Tuần
- **Thời gian**: 
  - 20h00 mỗi ngày
  - 2h55 sáng mỗi ngày
- **Channel**: 1435035898629591040
- **Nội dung**: Top 10 người học chăm chỉ nhất tuần này (Thứ 2 - Chủ nhật)

### 📅 Bảng Xếp Hạng Tháng
- **Thời gian**: 
  - Ngày 1 mỗi tháng lúc 2h50 sáng
  - Ngày 15 mỗi tháng lúc 2h50 sáng
- **Channel**: 1450690861036994763
- **Nội dung**: Top 10 người học chăm chỉ nhất tháng này

## ⚙️ Cấu hình

### Thay đổi Channel
Sửa trong `leaderboard_only_bot.py`:
```python
CHANNEL_DAILY = 1450690801934930124      # Channel bảng xếp hạng ngày
CHANNEL_WEEKLY = 1435035898629591040     # Channel bảng xếp hạng tuần
CHANNEL_MONTHLY = 1450690861036994763    # Channel bảng xếp hạng tháng
```

### Thay đổi Thời gian

#### Bảng xếp hạng ngày:
```python
@tasks.loop(time=time(hour=2, minute=58, tzinfo=VN_TZ))
async def auto_post_daily(self):
```
Thay `hour=2, minute=58` thành giờ bạn muốn.

#### Bảng xếp hạng tuần:
```python
# Trong hàm auto_post_weekly
if (current_hour == 20 and current_minute == 0) or (current_hour == 2 and current_minute == 55):
```
Thay `20` và `2, 55` thành giờ bạn muốn.

#### Bảng xếp hạng tháng:
```python
# Trong hàm auto_post_monthly
if (now.day == 1 or now.day == 15) and now.hour == 2 and now.minute == 50:
```
Thay `1, 15` (ngày) và `2, 50` (giờ) thành giá trị bạn muốn.

## 🧪 Test

### Xem log khi bot khởi động:
```
⏰ Đang khởi động scheduled tasks...
✅ Đã khởi động tất cả scheduled tasks
⏰ Task tuần sẽ chạy lần đầu vào 29/12/2025 20:00 (sau 5.2h)
```

### Xem log khi tự động gửi:
```
⏰ [AUTO] Đang gửi bảng xếp hạng ngày...
📡 Đang lấy dữ liệu bảng xếp hạng day...
✅ Đã lấy được 10 người dùng
🎨 Đang render bảng xếp hạng...
📊 Đã nhận image data: 123456 bytes
✅ [AUTO] Đã gửi bảng xếp hạng ngày
```

### Test ngay lập tức:
1. Sửa thời gian trong code thành giờ hiện tại + 1 phút
2. Restart bot: `python3 start.py`
3. Đợi 1 phút và xem channel
4. Nhớ đổi lại thời gian gốc sau khi test!

## ⚠️ Lưu ý

1. **Bot phải online 24/7** để tự động gửi hoạt động
2. **Quyền channel**: Bot cần quyền `Send Messages` và `Attach Files` trong các channel
3. **Múi giờ**: Tất cả thời gian theo múi giờ Việt Nam (UTC+7)
4. **Restart bot**: Sau khi thay đổi cấu hình, cần restart bot

## 🔍 Troubleshooting

### Không thấy tin nhắn tự động
1. Kiểm tra bot có online không
2. Kiểm tra quyền bot trong channel
3. Xem log có thông báo `[AUTO]` không
4. Kiểm tra Channel ID có đúng không

### Sai giờ gửi
1. Kiểm tra múi giờ server: `date`
2. Bot tự động xử lý múi giờ Việt Nam
3. Kiểm tra code có đúng `tzinfo=VN_TZ` không

### Lỗi khi gửi
Xem log chi tiết:
```
❌ [AUTO] Lỗi gửi bảng xếp hạng ngày: ...
```
Thường do:
- API không phản hồi
- GUI server chưa sẵn sàng
- Không có quyền gửi tin nhắn
