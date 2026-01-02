# 🔔 Hướng Dẫn Chi Tiết Hệ Thống Đánh Thức Học Tập

## 📖 Tổng Quan

Hệ thống đánh thức học tập là một tính năng thông minh giúp tạo động lực và thói quen học tập tốt cho cộng đồng. Hệ thống này bao gồm 6 loại đánh thức khác nhau, mỗi loại phục vụ một mục đích cụ thể.

## 🎯 6 Loại Đánh Thức

### 1. 🔔 Đánh Thức Tất Cả (`/danh-thuc`)

**Cách hoạt động:**
- Gửi tin nhắn `@everyone` trong channel hiện tại
- Hiển thị thời gian hiện tại và người đánh thức
- Bao gồm checklist học tập cụ thể
- Đề xuất phương pháp Pomodoro

**Nội dung mẫu:**
```
🔔 **ĐÁNH THỨC HỌC TẬP** 🔔

@everyone 

💪 **Thành công bắt đầu từ việc thức dậy sớm!** 💪

🕐 **Thời gian**: 14:30
👤 **Người đánh thức**: @YourName
📚 **Thông điệp**: Đã đến lúc học tập rồi! Hãy cùng nhau nỗ lực nhé!

**🎯 Hãy bắt đầu học ngay:**
• Mở sách/laptop
• Tập trung 100%
• Tắt điện thoại
• Uống nước, ngồi thẳng

**⏰ Pomodoro Suggestion:**
25 phút học → 5 phút nghỉ → Lặp lại

💪 *Cùng nhau tiến bộ mỗi ngày!* 💪
```

### 2. 🎯 Đánh Thức Cá Nhân (`/danh-thuc-user @user`)

**Cách hoạt động:**
- Tag một user cụ thể
- Kiểm tra trạng thái online/offline của user
- Nội dung cá nhân hóa với tên user
- Checklist riêng cho cá nhân

**Nội dung mẫu:**
```
⚡ **ĐÁNH THỨC CÁ NHÂN** ⚡

@UserName 🟢

🔥 **Kiến thức là sức mạnh, hãy tích lũy ngay!** 🔥

🕐 **Thời gian**: 14:30
👤 **Người đánh thức**: @YourName
🎯 **Mục tiêu**: Đã đến lúc UserName học tập rồi!

**📋 Checklist cho bạn:**
✅ Chuẩn bị tài liệu
✅ Tìm chỗ ngồi thoải mái  
✅ Đặt mục tiêu cụ thể
✅ Bắt đầu ngay!

🔥 *Bạn làm được mà! Fighting!* 🔥
```

### 3. 📢 Đánh Thức Kênh (`/danh-thuc-kenh`)

**Cách hoạt động:**
- Gửi vào kênh đánh thức chuyên dụng (ID: 1456243735938600970)
- Phong cách "emergency alert" thú vị
- Nội dung như báo động khẩn cấp
- Có timeline hành động cụ thể

**Nội dung mẫu:**
```
🔔🎺 **TIẾNG KÈNG HỌC TẬP** 🎺🔔

@everyone 

🔥 **EMERGENCY STUDY ALERT** 🔥

⭐ **Mỗi ngày học một chút, thành công sẽ đến!** ⭐

🕐 **Thời gian báo động**: 14:30
👤 **Chỉ huy trưởng**: @YourName
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

⭐ **AI KHÔNG HỌC BÂY GIỜ THÌ KHI NÀO?** ⭐

*Tin nhắn này sẽ tự hủy sau khi bạn bắt đầu học... 😄*
```

### 4. ⏰ Đánh Thức Hẹn Giờ (`/danh-thuc-hen-gio [phút] [tin nhắn]`)

**Cách hoạt động:**
- Tạo một task chạy ngầm sau X phút
- Cho phép tùy chỉnh tin nhắn
- Hiển thị thời gian đặt hẹn và thời gian thực hiện
- Tự động gửi tin nhắn khi đến giờ

**Ví dụ sử dụng:**
```
/danh-thuc-hen-gio 30 Làm bài tập Toán
```

**Nội dung khi đến giờ:**
```
⏰ **ĐÁNH THỨC HẸN GIỜ** ⏰

🔔 **Thông báo từ @YourName**

📝 **Nội dung**: Làm bài tập Toán
🕐 **Thời gian**: 15:00
⏱️ **Đã hẹn từ**: 30 phút trước

💪 **Đã đến lúc thực hiện cam kết của bạn!**
```

### 5. 🍅 Pomodoro Timer (`/danh-thuc-pomodoro [chu kỳ]`)

**Cách hoạt động:**
- Chạy chu kỳ 25 phút học + 5 phút nghỉ
- Tự động báo bắt đầu, nghỉ, và kết thúc
- Theo dõi tiến độ real-time
- Có thể chạy 1-8 chu kỳ

**Ví dụ sử dụng:**
```
/danh-thuc-pomodoro 3
```

**Tin nhắn bắt đầu chu kỳ:**
```
🍅 **POMODORO - CHU KỲ 1/3** 🍅

⏰ **BẮT ĐẦU HỌC**: 14:30
👤 **Người khởi tạo**: @YourName

📚 **25 PHÚT HỌC TẬP**
• Tập trung 100%
• Không kiểm tra điện thoại
• Không làm việc khác
• Chỉ học thôi!

⏰ **Sẽ báo nghỉ lúc**: 14:55

🔥 **FOCUS MODE ON!** 🔥
```

**Tin nhắn nghỉ ngơi:**
```
🛑 **POMODORO - NGHỈ NGƠI** 🛑

⏰ **GIỜ NGHỈ**: 14:55
🍅 **Hoàn thành chu kỳ**: 1/3

😌 **5 PHÚT NGHỈ NGƠI**
• Đứng dậy vận động
• Uống nước
• Thả lỏng mắt
• Thở sâu

⏰ **Chu kỳ tiếp theo**: 15:00

💪 **Bạn đang làm rất tốt!** 💪
```

**Tin nhắn kết thúc:**
```
🎉 **HOÀN THÀNH POMODORO** 🎉

⏰ **Kết thúc**: 16:00
🍅 **Tổng chu kỳ**: 3
⏱️ **Tổng thời gian học**: 75 phút

🏆 **CHÚC MỪNG @YourName!**

📈 **Thành tựu hôm nay:**
• Hoàn thành 3 Pomodoro
• Học tập 75 phút tập trung
• Xây dựng thói quen tốt

🎯 **Hãy tiếp tục duy trì!**
```

### 6. 📊 Thống Kê (`/danh-thuc-stats`)

**Cách hoạt động:**
- Hiển thị thống kê giả lập (chưa có database)
- Chỉ người dùng mới thấy được (ephemeral)
- Bao gồm số liệu và thành tựu
- Có lời khuyên cải thiện

**Nội dung mẫu:**
```
📊 **THỐNG KÊ ĐÁNH THỨC** 📊

👤 **Người dùng**: @YourName

📈 **Số liệu tổng quan:**
🔔 **Tổng lần đánh thức**: 25
📅 **Đánh thức hôm nay**: 3
⏰ **Giờ đánh thức yêu thích**: 14:30
🔥 **Streak hiện tại**: 7 ngày

🏆 **Thành tựu:**
🥈 Người đánh thức nhiệt tình

💪 **Động lực**: Bạn đã giúp cộng đồng học tập 25 lần!

⭐ **Mẹo**: Đánh thức đều đặn sẽ tạo thói quen tốt cho bản thân!
```

## 🎨 Tính Năng Đặc Biệt

### 🎲 Hệ Thống Ngẫu Nhiên

**Emoji đánh thức (10 loại):**
🔔 ⏰ 📢 🎺 🔊 ⚡ 💪 🚀 🎯 📚

**Emoji động viên (10 loại):**
💪 🔥 ⭐ 🏆 🎯 📈 💎 🚀 ⚡ 🌟

**Câu động viên (10 câu):**
1. "Thành công bắt đầu từ việc thức dậy sớm!"
2. "Mỗi phút trôi qua là một cơ hội học tập!"
3. "Hôm nay bạn sẽ học được điều gì mới?"
4. "Kiến thức là sức mạnh, hãy tích lũy ngay!"
5. "Đừng để thời gian trôi qua vô ích!"
6. "Học tập là đầu tư tốt nhất cho tương lai!"
7. "Mỗi ngày học một chút, thành công sẽ đến!"
8. "Hãy biến giấc mơ thành hiện thực!"
9. "Chỉ có học tập mới thay đổi cuộc đời!"
10. "Bắt đầu ngay bây giờ, đừng chờ đợi!"

### ⏰ Hệ Thống Cooldown

**Cách hoạt động:**
- Mỗi user có cooldown 5 phút (300 giây)
- Áp dụng cho tất cả loại đánh thức (trừ stats)
- Hiển thị thời gian còn lại nếu vi phạm
- Tránh spam và lạm dụng

**Thông báo cooldown:**
```
⏰ Bạn cần đợi 3m 45s nữa mới có thể đánh thức tiếp!
```

### 🎯 Nội Dung Thông Minh

**Theo thời gian:**
- Hiển thị thời gian hiện tại (múi giờ Việt Nam)
- Format: HH:MM (VD: 14:30)

**Theo trạng thái user:**
- 🟢 Online
- 🔴 Offline/Invisible/Do Not Disturb

**Theo loại đánh thức:**
- Nội dung khác nhau cho từng loại
- Phong cách phù hợp với mục đích

## 🔧 Cấu Hình Kỹ Thuật

### Channel và Cooldown
```python
WAKEUP_CHANNEL = 1456243735938600970  # Kênh đánh thức chuyên dụng
wakeup_cooldown_duration = 300        # 5 phút cooldown
```

### Pomodoro Settings
```python
STUDY_TIME = 25 * 60      # 25 phút học (1500 giây)
BREAK_TIME = 5 * 60       # 5 phút nghỉ (300 giây)
MAX_CYCLES = 8            # Tối đa 8 chu kỳ/lần
```

### Timer Settings
```python
MIN_MINUTES = 1           # Tối thiểu 1 phút
MAX_MINUTES = 1440        # Tối đa 24 giờ (1440 phút)
```

## 📋 Hướng Dẫn Sử Dụng

### Cách Sử Dụng Cơ Bản

1. **Đánh thức tất cả:**
   ```
   /danh-thuc
   ```

2. **Đánh thức một người:**
   ```
   /danh-thuc-user @tên_user
   ```

3. **Đánh thức vào kênh chuyên dụng:**
   ```
   /danh-thuc-kenh
   ```

4. **Hẹn giờ đánh thức:**
   ```
   /danh-thuc-hen-gio 30 Làm bài tập
   ```

5. **Chạy Pomodoro:**
   ```
   /danh-thuc-pomodoro 3
   ```

6. **Xem thống kê:**
   ```
   /danh-thuc-stats
   ```

### Mẹo Sử Dụng Hiệu Quả

**Thời điểm tốt nhất:**
- 🌅 **Sáng sớm**: 6h-8h (bắt đầu ngày mới)
- 🍽️ **Sau ăn trưa**: 13h-14h (tránh buồn ngủ)
- 🌙 **Tối**: 19h-21h (học buổi tối)

**Kết hợp với bạn bè:**
- Hẹn nhau cùng đánh thức
- Tạo nhóm học Pomodoro
- Thử thách ai đánh thức nhiều hơn

**Sử dụng hẹn giờ:**
- Đặt nhắc nhở trước khi học
- Nhắc nghỉ giải lao
- Báo deadline bài tập

**Pomodoro hiệu quả:**
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