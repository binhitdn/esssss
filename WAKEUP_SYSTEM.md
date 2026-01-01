# 🔔 Hệ Thống Đánh Thức Học Tập

Tính năng đánh thức học tập thông minh giúp tạo động lực và thói quen học tập tốt cho cộng đồng.

## 🎯 Các Loại Đánh Thức

### 1. 🔔 Đánh Thức Tất Cả (`/danh-thuc`)
- **Mục đích**: Đánh thức toàn bộ server (@everyone)
- **Sử dụng**: Khi muốn tạo không khí học tập chung
- **Nội dung**: Tin nhắn động viên + checklist học tập
- **Cooldown**: 5 phút/người để tránh spam

### 2. 🎯 Đánh Thức Cá Nhân (`/danh-thuc-user @user`)
- **Mục đích**: Đánh thức một người cụ thể
- **Sử dụng**: Nhắc nhở bạn bè học tập
- **Nội dung**: Tin nhắn cá nhân hóa + checklist riêng
- **Tính năng**: Hiển thị trạng thái online/offline của user

### 3. 📢 Đánh Thức Kênh (`/danh-thuc-kenh`)
- **Mục đích**: Gửi đánh thức vào kênh chuyên dụng
- **Kênh**: 1456243735938600970
- **Nội dung**: Thông báo khẩn cấp kiểu "báo động học tập"
- **Đặc biệt**: Có hiệu ứng "emergency alert" thú vị

### 4. ⏰ Đánh Thức Hẹn Giờ (`/danh-thuc-hen-gio [phút] [tin nhắn]`)
- **Mục đích**: Đặt lịch đánh thức sau X phút
- **Thời gian**: 1-1440 phút (tối đa 24 giờ)
- **Tùy chỉnh**: Có thể thêm tin nhắn riêng
- **Sử dụng**: "Sau 30 phút nhắc tôi làm bài tập"

### 5. 🍅 Pomodoro Timer (`/danh-thuc-pomodoro [chu kỳ]`)
- **Phương pháp**: 25 phút học + 5 phút nghỉ
- **Chu kỳ**: 1-8 chu kỳ/lần
- **Tự động**: Bot tự báo bắt đầu/nghỉ/kết thúc
- **Động lực**: Theo dõi tiến độ real-time

### 6. 📊 Thống Kê (`/danh-thuc-stats`)
- **Nội dung**: Số lần đánh thức, streak, giờ yêu thích
- **Thành tựu**: Huy hiệu dựa trên hoạt động
- **Cá nhân**: Chỉ người dùng mới thấy được

## 🎨 Tính Năng Đặc Biệt

### 🎲 Nội Dung Ngẫu Nhiên
- **10 emoji đánh thức**: 🔔⏰📢🎺🔊⚡💪🚀🎯📚
- **10 emoji động viên**: 💪🔥⭐🏆🎯📈💎🚀⚡🌟
- **10 câu động viên**: Thay đổi mỗi lần sử dụng

### ⏰ Hệ Thống Cooldown
- **Thời gian**: 5 phút/người
- **Mục đích**: Tránh spam và lạm dụng
- **Thông báo**: Hiển thị thời gian còn lại nếu vi phạm

### 🎯 Nội Dung Thông Minh
- **Theo thời gian**: Hiển thị giờ hiện tại
- **Theo trạng thái**: Kiểm tra user online/offline
- **Theo loại**: Nội dung khác nhau cho từng loại đánh thức

## 📋 Hướng Dẫn Sử Dụng

### Đánh Thức Cơ Bản
```
/danh-thuc
```
→ Đánh thức tất cả mọi người

### Đánh Thức Cá Nhân
```
/danh-thuc-user @TenUser
```
→ Đánh thức user cụ thể

### Hẹn Giờ Đánh Thức
```
/danh-thuc-hen-gio 30 Làm bài tập Toán
```
→ Sau 30 phút sẽ nhắc làm bài tập Toán

### Pomodoro
```
/danh-thuc-pomodoro 3
```
→ Chạy 3 chu kỳ Pomodoro (75 phút học + 10 phút nghỉ)

## 🎯 Mẹo Sử Dụng Hiệu Quả

### 1. **Thời Điểm Tốt Nhất**
- **Sáng sớm**: 6h-8h (bắt đầu ngày mới)
- **Sau ăn trưa**: 13h-14h (tránh buồn ngủ)
- **Tối**: 19h-21h (học buổi tối)

### 2. **Kết Hợp Với Bạn Bè**
- Hẹn nhau cùng đánh thức
- Tạo nhóm học Pomodoro
- Thử thách ai đánh thức nhiều hơn

### 3. **Sử Dụng Hẹn Giờ**
- Đặt nhắc nhở trước khi học
- Nhắc nghỉ giải lao
- Báo deadline bài tập

### 4. **Pomodoro Hiệu Quả**
- Bắt đầu với 1-2 chu kỳ
- Tăng dần lên 4-6 chu kỳ
- Nghỉ dài 15-30p sau 4 chu kỳ

## ⚠️ Lưu Ý Quan Trọng

### 🚫 Không Spam
- Cooldown 5 phút/người
- Sử dụng có ý thức
- Tôn trọng thành viên khác

### 🎯 Sử Dụng Đúng Mục Đích
- Chỉ đánh thức để học tập
- Không dùng để làm phiền
- Nội dung tích cực, lành mạnh

### 📱 Quyền Riêng Tư
- Stats chỉ bản thân thấy được
- Không lưu trữ nội dung cá nhân
- Tôn trọng sự riêng tư

## 🔧 Cấu Hình Kỹ Thuật

### Channel ID
```python
WAKEUP_CHANNEL = 1456243735938600970  # Kênh đánh thức chuyên dụng
```

### Cooldown Settings
```python
wakeup_cooldown_duration = 300  # 5 phút = 300 giây
```

### Pomodoro Settings
- **Học**: 25 phút (1500 giây)
- **Nghỉ ngắn**: 5 phút (300 giây)
- **Chu kỳ tối đa**: 8 chu kỳ/lần

## 🎉 Tương Lai

### Tính Năng Sắp Có
- 📊 **Database thống kê**: Lưu trữ lâu dài
- 🏆 **Hệ thống huy hiệu**: Thành tựu đánh thức
- 🎵 **Âm thanh đánh thức**: Voice alerts
- 📅 **Lịch đánh thức**: Đặt lịch hàng ngày
- 🤖 **AI đánh thức**: Nội dung thông minh hơn

### Ý Tưởng Mở Rộng
- **Study buddy matching**: Ghép đôi học tập
- **Group challenges**: Thử thách nhóm
- **Mood-based wakeup**: Đánh thức theo tâm trạng
- **Smart scheduling**: AI đề xuất thời gian học

---

💡 **Mẹo**: Hãy sử dụng đánh thức như một công cụ tạo động lực tích cực, không phải để làm phiền người khác!

🎯 **Mục tiêu**: Xây dựng cộng đồng học tập năng động và hỗ trợ lẫn nhau!