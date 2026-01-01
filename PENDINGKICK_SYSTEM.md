# 🚨 Hệ Thống PendingKick Tự Động

Hệ thống tự động gửi thông báo cho thành viên có role PendingKick và quản lý tin nhắn thông minh.

## 🎯 Tổng Quan

### Mục Đích
- Thông báo cho thành viên PendingKick về tình trạng của họ
- Hướng dẫn cách quay lại hoặc rời khỏi server
- Tự động gửi và xóa tin nhắn theo lịch trình
- Giảm thiểu spam và quản lý tin nhắn hiệu quả

### Quy Trình Hoạt Động
```
6:00 AM → Tìm role PendingKick → Tag tất cả members → Lưu message ID → 2:51 AM hôm sau → Xóa tin nhắn
```

## ⏰ Lịch Trình Tự Động

### 🌅 6:00 AM - Gửi Thông Báo PendingKick
- **Thời gian**: 6h00 sáng mỗi ngày (múi giờ Việt Nam)
- **Hành động**: Tìm tất cả thành viên có role PendingKick và gửi thông báo
- **Channel**: 1446655276962021497
- **Role**: 1436802180429385768

### 🌙 2:51 AM - Xóa Tin Nhắn
- **Thời gian**: 2h51 sáng hôm sau
- **Hành động**: Tự động xóa tin nhắn PendingKick
- **Lý do**: Tránh spam và giữ channel sạch sẽ

## 📝 Nội Dung Tin Nhắn

### Template PendingKick
```
🚨 **THÔNG BÁO PENDINGKICK** 🚨

@user1 @user2 @user3 ...

Bạn đã được chuyển sang **PendingKick** do không học đủ mục tiêu **2 ngày liên tiếp**.

🔄 **Vui lòng nhấp vào nút "Xin quay lại" ở trên** nếu cậu muốn tiếp tục học với tụi mình hoặc tự rời khỏi nhóm.

💭 **(Sẽ không có thông báo nào cho ai kể cả admin nên cậu cứ thoải mái ạ)**

---
*Tin nhắn này sẽ tự động xóa vào 2h51 sáng ngày mai.*
```

### Thông Tin Động
- **@mentions**: Tự động tag tất cả thành viên có role PendingKick
- **Số lượng**: Hiển thị trong log số thành viên được tag
- **Thời gian**: Tự động tính thời gian xóa

## 🔧 Cấu Hình Hệ Thống

### Constants
```python
PENDINGKICK_ROLE_ID = 1436802180429385768    # Role PendingKick
PENDINGKICK_CHANNEL_ID = 1446655276962021497 # Channel gửi thông báo
```

### Thời Gian
- **Gửi**: 6:00 AM (UTC+7)
- **Xóa**: 2:51 AM ngày hôm sau (UTC+7)
- **Kiểm tra**: Mỗi 30 giây

## 🎮 Lệnh Admin

### 1. 🧪 Test PendingKick (`/test-pendingkick`)
**Quyền**: Chỉ Administrator
**Chức năng**: Gửi tin nhắn PendingKick ngay lập tức để test
**Sử dụng**: Kiểm tra format và hoạt động của hệ thống

### 2. 🗑️ Xóa PendingKick (`/xoa-pendingkick`)
**Quyền**: Chỉ Administrator  
**Chức năng**: Xóa tất cả tin nhắn PendingKick đang theo dõi
**Sử dụng**: Dọn dẹp khi cần thiết

### 3. 📊 Trạng Thái (`/pendingkick-status`)
**Quyền**: Chỉ Administrator
**Chức năng**: Xem thông tin chi tiết về hệ thống
**Hiển thị**:
- Thời gian hiện tại
- Thời gian gửi/xóa tiếp theo
- Số thành viên PendingKick hiện tại
- Số tin nhắn đang theo dõi
- Cấu hình hệ thống

### 4. 👥 Danh Sách (`/list-pendingkick`)
**Quyền**: Chỉ Administrator
**Chức năng**: Xem danh sách thành viên có role PendingKick
**Hiển thị**:
- Tên và mention của từng thành viên
- Tổng số thành viên
- Giới hạn 20 thành viên đầu tiên

## 🔄 Vòng Đời Tin Nhắn

### 1. Gửi Tin Nhắn (6:00 AM)
```
1. Kiểm tra thời gian = 6:00 AM
2. Lấy guild và role PendingKick
3. Tìm tất cả members có role này
4. Tạo danh sách mentions
5. Tạo nội dung thông báo
6. Gửi tin nhắn vào channel
7. Lưu message ID + thời gian xóa + số lượng members
8. Log thành công
```

### 2. Theo Dõi Tin Nhắn
```
bot.pendingkick_messages = {
    message_id: {
        'delete_time': datetime(2026, 1, 3, 2, 51, 0),
        'channel_id': 1446655276962021497,
        'sent_time': datetime(2026, 1, 2, 6, 0, 0),
        'member_count': 5
    }
}
```

### 3. Xóa Tin Nhắn (2:51 AM)
```
1. Kiểm tra thời gian = 2:51 AM
2. Duyệt danh sách tin nhắn PendingKick
3. Kiểm tra thời gian xóa
4. Fetch và delete message
5. Xóa khỏi danh sách theo dõi
6. Log kết quả
```

## 📊 Ví Dụ Thực Tế

### Scenario: Một Ngày Hoạt Động
```
[2/1/2026 - 6:00 AM]
System: Tìm thấy 3 thành viên có role PendingKick
Bot: 🚨 THÔNG BÁO PENDINGKICK - @Alice @Bob @Charlie
System: Lưu message ID 987654321, xóa lúc 3/1/2026 2:51 AM

[3/1/2026 - 2:51 AM]  
System: Kiểm tra message 987654321 → Đến giờ xóa
Bot: Xóa message 987654321
System: Xóa khỏi danh sách theo dõi
```

### Scenario: Không Có Thành Viên PendingKick
```
[2/1/2026 - 6:00 AM]
System: Tìm role PendingKick...
System: 📭 Không có thành viên nào có role PendingKick
System: Bỏ qua gửi thông báo
```

### Scenario: Test Bởi Admin
```
Admin: /test-pendingkick
Bot: 🧪 Đang test hệ thống PendingKick...
System: Tìm thấy 2 thành viên có role PendingKick
Bot: Gửi tin nhắn PendingKick test
Bot: ✅ Đã gửi tin nhắn PendingKick test!

Admin: /list-pendingkick
Bot: 👥 DANH SÁCH THÀNH VIÊN PENDINGKICK
     1. **Alice** (@Alice)
     2. **Bob** (@Bob)
     Tổng số: 2 thành viên

Admin: /pendingkick-status
Bot: 📊 TRẠNG THÁI HỆ THỐNG PENDINGKICK
     👥 Thành viên PendingKick hiện tại: 2
     📊 Tin nhắn đang theo dõi: 1
```

## 🚨 Xử Lý Lỗi

### Lỗi Thường Gặp

**1. Channel không tồn tại**
```
❌ Không tìm thấy channel PendingKick 1446655276962021497
```

**2. Role không tồn tại**
```
❌ Không tìm thấy role PendingKick 1436802180429385768
```

**3. Không có thành viên nào có role**
```
📭 Không có thành viên nào có role PendingKick
→ Bỏ qua gửi thông báo
```

**4. Tin nhắn đã bị xóa**
```
⚠️ Tin nhắn 987654321 đã bị xóa trước đó
→ Tự động xóa khỏi danh sách theo dõi
```

**5. Không có quyền xóa**
```
❌ Lỗi xóa tin nhắn 987654321: Missing Permissions
```

### Khắc Phục
- Kiểm tra quyền bot trong channel
- Đảm bảo role PendingKick tồn tại
- Kiểm tra ID role và channel
- Đảm bảo bot online 24/7
- Sử dụng `/xoa-pendingkick` để dọn dẹp thủ công

## 💡 Tính Năng Thông Minh

### 1. **Tự Động Tìm Members**
```python
pendingkick_members = [member for member in guild.members if role in member.roles]
```

### 2. **Tạo Mentions Động**
```python
member_mentions = " ".join([member.mention for member in pendingkick_members])
```

### 3. **Theo Dõi Số Lượng**
```python
self.pendingkick_messages[message.id] = {
    'member_count': len(pendingkick_members)
}
```

### 4. **Kiểm Tra Trống**
```python
if not pendingkick_members:
    print("📭 Không có thành viên nào có role PendingKick")
    return
```

### 5. **Giới Hạn Hiển Thị**
```python
# Trong list command, giới hạn 20 thành viên
if i >= 20:
    member_list += f"... và {len(pendingkick_members) - 20} thành viên khác\n"
    break
```

## 🔮 So Sánh Với Warning System

### Điểm Giống
- Cùng thời gian gửi (6:00 AM) và xóa (2:51 AM)
- Cùng cơ chế theo dõi và xóa tin nhắn
- Cùng có lệnh admin để test và quản lý

### Điểm Khác
| Tính năng | Warning | PendingKick |
|-----------|---------|-------------|
| **Target** | 1 user cụ thể | Tất cả members có role |
| **Nội dung** | Cảnh báo học tập | Thông báo PendingKick |
| **Mục đích** | Nhắc nhở học | Hướng dẫn quay lại/rời |
| **Tone** | Nghiêm khắc | Nhẹ nhàng, thân thiện |

## 🔮 Tương Lai

### Tính Năng Sắp Có
- **📊 Database**: Lưu trữ lịch sử PendingKick
- **📱 DM**: Gửi tin nhắn riêng cho từng thành viên
- **🎯 Custom message**: Nội dung tùy chỉnh theo thành viên
- **📅 Flexible schedule**: Tùy chỉnh thời gian gửi/xóa
- **🔔 Escalation**: Tăng cường thông báo theo thời gian

### Ý Tưởng Mở Rộng
- **Smart timing**: AI chọn thời gian gửi tối ưu
- **Personalized**: Nội dung cá nhân hóa theo lý do PendingKick
- **Analytics**: Thống kê tỷ lệ quay lại vs rời đi
- **Integration**: Tích hợp với hệ thống quản lý thành viên

## ⚙️ Cấu Hình Nâng Cao

### Thay Đổi Thời Gian Gửi
```python
# Trong pendingkick_system_loop()
if now.hour == 6 and now.minute == 0:  # Thay 6 thành giờ khác
```

### Thay Đổi Thời Gian Xóa
```python
# Trong pendingkick_system_loop()  
elif now.hour == 2 and now.minute == 51:  # Thay 2, 51 thành giờ/phút khác
```

### Thay Đổi Role/Channel
```python
PENDINGKICK_ROLE_ID = 1436802180429385768    # Thay ID role
PENDINGKICK_CHANNEL_ID = 1446655276962021497 # Thay ID channel
```

### Tùy Chỉnh Nội Dung
```python
# Trong send_pendingkick_message()
pendingkick_content = f"""
🚨 **THÔNG BÁO TÙY CHỈNH** 🚨
{custom_content}
"""
```

### Thay Đổi Giới Hạn Hiển Thị
```python
# Trong list_pendingkick_command()
if i >= 50:  # Thay 20 thành 50 hoặc số khác
```

---

💡 **Lưu ý**: Hệ thống này hoạt động tự động 24/7 và chỉ gửi thông báo khi có thành viên có role PendingKick. Đảm bảo bot có quyền đọc role và gửi tin nhắn trong channel được cấu hình.

🎯 **Mục tiêu**: Tạo cơ hội cho thành viên PendingKick quay lại một cách nhẹ nhàng và thân thiện, đồng thời giữ channel sạch sẽ và không spam!