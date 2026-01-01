# ⚠️ Hệ Thống Cảnh Báo Tự Động

Hệ thống tự động gửi cảnh báo học tập và quản lý tin nhắn thông minh.

## 🎯 Tổng Quan

### Mục Đích
- Nhắc nhở user có warning về việc học tập
- Tự động gửi và xóa tin nhắn theo lịch trình
- Giảm thiểu spam và quản lý tin nhắn hiệu quả

### Quy Trình Hoạt Động
```
6:00 AM → Gửi cảnh báo → Lưu message ID → 2:51 AM hôm sau → Xóa tin nhắn
```

## ⏰ Lịch Trình Tự Động

### 🌅 6:00 AM - Gửi Cảnh Báo
- **Thời gian**: 6h00 sáng mỗi ngày (múi giờ Việt Nam)
- **Hành động**: Gửi tin nhắn cảnh báo tag user
- **Channel**: 1446655389860106361
- **User**: 1436409040036040886

### 🌙 2:51 AM - Xóa Tin Nhắn
- **Thời gian**: 2h51 sáng hôm sau
- **Hành động**: Tự động xóa tin nhắn cảnh báo
- **Lý do**: Tránh spam và giữ channel sạch sẽ

## 📝 Nội Dung Tin Nhắn

### Template Cảnh Báo
```
⚠️ **CẢNH BÁO HỌC TẬP** ⚠️

<@1436409040036040886>

Các bạn đã bị gắn **Warning** vì vậy hãy học đủ thời gian mục tiêu trước **3h sáng ngày {ngày mai}** trước khi bị chuyển sang **pendingKick**.

📊 **Để biết thời gian mục tiêu của mình là bao nhiêu:**
🔗 Truy cập: https://14study.io.vn

⚠️ **Lưu ý:** Nếu bạn không cài đặt thì mặc định là **1 giờ**.

🎯 **Hãy nỗ lực học tập để tránh bị kick khỏi server!**

---
*Tin nhắn này sẽ tự động xóa vào 2h51 sáng ngày mai.*
```

### Thông Tin Động
- **{ngày mai}**: Tự động tính toán ngày hôm sau (DD/MM/YYYY)
- **User tag**: Tự động tag user có ID được cấu hình
- **Thời gian**: Hiển thị chính xác thời gian deadline

## 🔧 Cấu Hình Hệ Thống

### Constants
```python
WARNING_USER_ID = 1436409040036040886        # User cần tag
WARNING_CHANNEL_ID = 1446655389860106361     # Channel gửi warning
```

### Thời Gian
- **Gửi**: 6:00 AM (UTC+7)
- **Xóa**: 2:51 AM ngày hôm sau (UTC+7)
- **Kiểm tra**: Mỗi 30 giây

## 🎮 Lệnh Admin

### 1. 🧪 Test Warning (`/test-warning`)
**Quyền**: Chỉ Administrator
**Chức năng**: Gửi tin nhắn cảnh báo ngay lập tức để test
**Sử dụng**: Kiểm tra format và hoạt động của hệ thống

### 2. 🗑️ Xóa Warning (`/xoa-warning`)
**Quyền**: Chỉ Administrator  
**Chức năng**: Xóa tất cả tin nhắn cảnh báo đang theo dõi
**Sử dụng**: Dọn dẹp khi cần thiết

### 3. 📊 Trạng Thái (`/warning-status`)
**Quyền**: Chỉ Administrator
**Chức năng**: Xem thông tin chi tiết về hệ thống
**Hiển thị**:
- Thời gian hiện tại
- Thời gian gửi/xóa tiếp theo
- Số tin nhắn đang theo dõi
- Cấu hình hệ thống

## 🔄 Vòng Đời Tin Nhắn

### 1. Gửi Tin Nhắn (6:00 AM)
```
1. Kiểm tra thời gian = 6:00 AM
2. Tính ngày mai
3. Tạo nội dung cảnh báo
4. Gửi tin nhắn vào channel
5. Lưu message ID + thời gian xóa
6. Log thành công
```

### 2. Theo Dõi Tin Nhắn
```
bot.warning_messages = {
    message_id: {
        'delete_time': datetime(2026, 1, 3, 2, 51, 0),
        'channel_id': 1446655389860106361,
        'sent_time': datetime(2026, 1, 2, 6, 0, 0)
    }
}
```

### 3. Xóa Tin Nhắn (2:51 AM)
```
1. Kiểm tra thời gian = 2:51 AM
2. Duyệt danh sách tin nhắn
3. Kiểm tra thời gian xóa
4. Fetch và delete message
5. Xóa khỏi danh sách theo dõi
6. Log kết quả
```

## 📊 Ví Dụ Thực Tế

### Scenario: Một Ngày Hoạt Động
```
[2/1/2026 - 6:00 AM]
Bot: ⚠️ CẢNH BÁO HỌC TẬP - @User học đủ trước 3h sáng ngày 3/1/2026
System: Lưu message ID 123456789, xóa lúc 3/1/2026 2:51 AM

[3/1/2026 - 2:51 AM]  
System: Kiểm tra message 123456789 → Đến giờ xóa
Bot: Xóa message 123456789
System: Xóa khỏi danh sách theo dõi
```

### Scenario: Test Bởi Admin
```
Admin: /test-warning
Bot: 🧪 Đang test hệ thống cảnh báo...
Bot: Gửi tin nhắn cảnh báo test
Bot: ✅ Đã gửi tin nhắn cảnh báo test!

Admin: /warning-status
Bot: 📊 TRẠNG THÁI HỆ THỐNG CẢNH BÁO
     ⏰ Thời gian hiện tại: 14:30:25 02/01/2026
     🔔 Gửi cảnh báo tiếp theo: 06:00 03/01/2026
     📊 Tin nhắn đang theo dõi: 1
```

## 🚨 Xử Lý Lỗi

### Lỗi Thường Gặp

**1. Channel không tồn tại**
```
❌ Không tìm thấy channel warning 1446655389860106361
```

**2. Tin nhắn đã bị xóa**
```
⚠️ Tin nhắn 123456789 đã bị xóa trước đó
→ Tự động xóa khỏi danh sách theo dõi
```

**3. Không có quyền xóa**
```
❌ Lỗi xóa tin nhắn 123456789: Missing Permissions
```

**4. Bot offline trong thời gian xóa**
```
→ Tin nhắn sẽ được xóa khi bot online lại
→ Hệ thống kiểm tra liên tục mỗi 30 giây
```

### Khắc Phục
- Kiểm tra quyền bot trong channel
- Đảm bảo bot online 24/7
- Sử dụng `/xoa-warning` để dọn dẹp thủ công
- Kiểm tra ID channel và user

## 💡 Tính Năng Thông Minh

### 1. **Tự Động Tính Ngày**
```python
tomorrow = datetime.now(vn_tz) + timedelta(days=1)
tomorrow_str = tomorrow.strftime('%d/%m/%Y')
```

### 2. **Theo Dõi Tin Nhắn**
```python
self.warning_messages[message.id] = {
    'delete_time': delete_time,
    'channel_id': channel.id,
    'sent_time': datetime.now(vn_tz)
}
```

### 3. **Xử Lý Múi Giờ**
```python
vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.now(vn_tz)
```

### 4. **Cooldown Tránh Spam**
```python
# Đợi 2 phút sau khi gửi/xóa để tránh lặp lại
await asyncio.sleep(120)
```

## 🔮 Tương Lai

### Tính Năng Sắp Có
- **📊 Database**: Lưu trữ lịch sử cảnh báo
- **📱 Webhook**: Thông báo qua Discord webhook
- **🎯 Multi-user**: Hỗ trợ nhiều user cùng lúc
- **📅 Flexible schedule**: Tùy chỉnh thời gian gửi/xóa
- **🔔 Escalation**: Tăng cường cảnh báo theo mức độ

### Ý Tưởng Mở Rộng
- **Smart timing**: AI chọn thời gian gửi tối ưu
- **Personalized**: Nội dung cá nhân hóa theo user
- **Analytics**: Thống kê hiệu quả cảnh báo
- **Integration**: Tích hợp với hệ thống học tập

## ⚙️ Cấu Hình Nâng Cao

### Thay Đổi Thời Gian Gửi
```python
# Trong warning_system_loop()
if now.hour == 6 and now.minute == 0:  # Thay 6 thành giờ khác
```

### Thay Đổi Thời Gian Xóa
```python
# Trong warning_system_loop()  
elif now.hour == 2 and now.minute == 51:  # Thay 2, 51 thành giờ/phút khác
```

### Thay Đổi User/Channel
```python
WARNING_USER_ID = 1436409040036040886        # Thay ID user
WARNING_CHANNEL_ID = 1446655389860106361     # Thay ID channel
```

### Tùy Chỉnh Nội dung
```python
# Trong send_warning_message()
warning_content = f"""
⚠️ **CẢNH BÁO TÙY CHỈNH** ⚠️
{custom_content}
"""
```

---

💡 **Lưu ý**: Hệ thống này hoạt động tự động 24/7. Đảm bảo bot có quyền gửi tin nhắn và xóa tin nhắn trong channel được cấu hình.

🎯 **Mục tiêu**: Tạo áp lực tích cực để khuyến khích học tập, đồng thời giữ channel sạch sẽ và không spam!