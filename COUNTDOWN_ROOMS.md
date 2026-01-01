# 📚 Hệ Thống Phòng Học Đếm Ngược

Tính năng tạo phòng voice đếm ngược đến ngày mục tiêu, giúp tạo động lực và theo dõi tiến độ học tập.

## 🎯 Tổng Quan

### Mục Đích
- Tạo động lực học tập bằng việc hiển thị thời gian còn lại
- Tạo không gian riêng cho từng mục tiêu học tập
- Theo dõi tiến độ một cách trực quan

### Đặc Điểm
- **Tự động cập nhật**: Tên phòng cập nhật mỗi phút
- **Quyền riêng**: Creator có full quyền, người khác chỉ xem
- **Tự động xóa**: Phòng tự xóa khi đến ngày mục tiêu
- **Đa định dạng**: Hỗ trợ 2 kiểu hiển thị tên phòng

## 🔧 Các Lệnh

### 1. 🏗️ Tạo Phòng (`/tao-phong-hoc`)

**Cú pháp:**
```
/tao-phong-hoc [tên] [ngày] [định dạng]
```

**Tham số:**
- **tên**: Tên mục tiêu (VD: JLPT, Thi cuối kỳ, Tốt nghiệp)
- **ngày**: Ngày mục tiêu (DD/MM/YYYY hoặc D/M/YYYY)
- **định dạng**: "full" hoặc "countdown"

**Ví dụ:**
```
/tao-phong-hoc "JLPT N2" "9/12/2025" "full"
→ Tạo phòng: "JLPT N2 Còn 125d22h23p"

/tao-phong-hoc "Thi cuối kỳ" "15/1/2026" "countdown"  
→ Tạo phòng: "89d15h42p"
```

### 2. 🗑️ Xóa Phòng (`/xoa-phong-hoc`)

**Cú pháp:**
```
/xoa-phong-hoc
```

**Chức năng:**
- Xóa phòng đếm ngược của bạn
- Nếu có nhiều phòng, hiển thị danh sách
- Chỉ creator mới có thể xóa

### 3. 📋 Danh Sách Phòng (`/danh-sach-phong-hoc`)

**Cú pháp:**
```
/danh-sach-phong-hoc
```

**Hiển thị:**
- Phòng của bạn (có thể quản lý)
- Phòng của thành viên khác (chỉ xem)
- Thời gian còn lại của từng phòng

## 🎨 Định Dạng Hiển Thị

### Format "full" (Mặc định)
```
Tên + Còn + Thời gian
VD: "JLPT N2 Còn 125d22h23p"
```

### Format "countdown"
```
Chỉ thời gian
VD: "125d22h23p"
```

### Ý Nghĩa Ký Hiệu
- **d**: ngày (days)
- **h**: giờ (hours) 
- **p**: phút (minutes)

## 📅 Định Dạng Ngày

### Hỗ Trợ
- **DD/MM/YYYY**: 09/12/2025
- **D/M/YYYY**: 9/12/2025
- **DD/MM/YY**: 09/12/25 (tự động thành 2025)

### Lưu Ý
- Ngày phải trong tương lai
- Thời gian mặc định: 23:59:59 của ngày đó
- Múi giờ: Việt Nam (UTC+7)

## 🔐 Hệ Thống Quyền

### Creator (Người Tạo)
- ✅ **Xem phòng**: Có thể thấy phòng
- ✅ **Kết nối**: Có thể vào phòng voice
- ✅ **Gửi tin nhắn**: Có thể chat trong phòng
- ✅ **Quản lý phòng**: Đổi tên, xóa phòng
- ✅ **Quản lý tin nhắn**: Xóa, pin tin nhắn

### Thành Viên Khác
- ✅ **Xem phòng**: Có thể thấy phòng trong danh sách
- ❌ **Kết nối**: Không thể vào phòng voice
- ❌ **Gửi tin nhắn**: Không thể chat

## ⚙️ Cấu Hình Hệ Thống

### Giới Hạn
- **Tối đa 3 phòng/người**: Tránh spam
- **Thời gian tối thiểu**: 1 phút trong tương lai
- **Thời gian tối đa**: Không giới hạn

### Danh Mục
```python
STUDY_ROOMS_CATEGORY = 1436215086694924449  # ID danh mục
```

### Cập Nhật
- **Tần suất**: Mỗi 60 giây
- **Độ chính xác**: Đến phút
- **Tự động**: Không cần can thiệp

## 🔄 Vòng Đời Phòng

### 1. Tạo Phòng
```
User dùng /tao-phong-hoc
→ Validate thông tin
→ Tạo voice channel với quyền
→ Lưu vào bot.countdown_rooms
→ Bắt đầu countdown
```

### 2. Cập Nhật
```
Mỗi 60 giây:
→ Tính thời gian còn lại
→ Tạo tên mới
→ Cập nhật tên channel
```

### 3. Kết Thúc
```
Khi hết thời gian:
→ Gửi thông báo chúc mừng
→ Đợi 30 giây
→ Xóa channel
→ Xóa khỏi bot.countdown_rooms
```

## 📊 Ví Dụ Thực Tế

### Scenario 1: Chuẩn Bị Thi JLPT
```
[Ngày 1/11/2025]
User: /tao-phong-hoc "JLPT N2" "7/12/2025" "full"
Bot: ✅ Tạo phòng "JLPT N2 Còn 36d15h23p"

[Mỗi ngày tên phòng tự động thay đổi]
2/11: "JLPT N2 Còn 35d15h23p"
3/11: "JLPT N2 Còn 34d15h23p"
...
6/12: "JLPT N2 Còn 1d15h23p"
7/12: "JLPT N2 Còn 0d02h15p"

[Khi đến 23:59:59 ngày 7/12]
Bot: 🎉 ĐÃ ĐẾN NGÀY JLPT N2! Phòng sẽ tự động xóa...
[Xóa phòng sau 30 giây]
```

### Scenario 2: Nhiều Mục Tiêu
```
User tạo 3 phòng:
1. "IELTS Còn 45d12h30p" (15/1/2026)
2. "Thi cuối kỳ Còn 20d08h15p" (21/12/2025)  
3. "89d22h45p" (format countdown cho deadline khác)

User: /danh-sach-phong-hoc
Bot: Hiển thị cả 3 phòng với thời gian còn lại
```

## 🚨 Xử Lý Lỗi

### Lỗi Thường Gặp

**1. Ngày không hợp lệ**
```
❌ Định dạng ngày không hợp lệ!
Hỗ trợ: DD/MM/YYYY hoặc D/M/YYYY
Ví dụ: 9/12/2025, 09/12/2025
```

**2. Ngày trong quá khứ**
```
❌ Ngày mục tiêu phải trong tương lai!
```

**3. Quá giới hạn phòng**
```
❌ Bạn chỉ có thể tạo tối đa 3 phòng đếm ngược!
```

**4. Không tìm thấy danh mục**
```
❌ Không tìm thấy danh mục phòng học!
```

### Khắc Phục
- Kiểm tra định dạng ngày
- Đảm bảo ngày trong tương lai
- Xóa phòng cũ trước khi tạo mới
- Kiểm tra ID danh mục trong code

## 💡 Mẹo Sử Dụng

### 1. **Đặt Tên Hiệu Quả**
```
✅ Tốt: "JLPT N2", "Thi cuối kỳ Toán", "Deadline báo cáo"
❌ Tránh: "abc", "test", "phòng của tôi"
```

### 2. **Chọn Định Dạng Phù Hợp**
```
"full": Khi muốn mọi người biết mục tiêu
"countdown": Khi muốn gọn gàng, chỉ cần thời gian
```

### 3. **Quản Lý Nhiều Phòng**
```
- Đặt tên khác nhau để dễ phân biệt
- Ưu tiên mục tiêu quan trọng nhất
- Xóa phòng không cần thiết
```

### 4. **Tận Dụng Quyền Creator**
```
- Dùng phòng như không gian riêng
- Ghi chú tiến độ trong chat
- Mời bạn bè vào khi cần (bằng cách cấp quyền)
```

## 🔮 Tương Lai

### Tính Năng Sắp Có
- **📊 Thống kê**: Theo dõi thời gian sử dụng phòng
- **🎵 Nhạc nền**: Phát nhạc focus tự động
- **📝 Ghi chú**: Lưu tiến độ học tập
- **👥 Chia sẻ**: Cho phép người khác vào phòng
- **🏆 Thành tựu**: Huy hiệu khi hoàn thành mục tiêu

### Ý Tưởng Mở Rộng
- **Nhắc nhở**: Bot nhắc khi gần đến hạn
- **Milestone**: Báo cáo khi còn 30d, 7d, 1d
- **Template**: Mẫu phòng có sẵn cho các kỳ thi phổ biến
- **Backup**: Lưu lịch sử các phòng đã hoàn thành

---

💡 **Lưu ý**: Hệ thống này giúp tạo động lực học tập bằng cách hiển thị trực quan thời gian còn lại. Hãy sử dụng một cách tích cực và có trách nhiệm!

🎯 **Mục tiêu**: Biến áp lực thành động lực, biến thời gian thành thành tựu!