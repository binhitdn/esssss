# StudyLion Bot Tiếng Việt - Hướng Dẫn Hoàn Chỉnh

## 🎉 HOÀN THÀNH!

Bot StudyLion tiếng Việt đã sẵn sàng với GUI gốc và dữ liệu giả!

## 🚀 Khởi Động Nhanh

```bash
# Khởi động bot (cách đơn giản nhất)
venv/bin/python run_simple_bot.py
```

## ✨ Tính Năng Hoàn Chỉnh

- ✅ **GUI Gốc**: Sử dụng GUI server gốc của LionBot
- ✅ **Render Ảnh**: Bảng xếp hạng với ảnh đẹp như gốc
- ✅ **Tiếng Việt**: Giao diện hoàn toàn tiếng Việt
- ✅ **Dữ Liệu Giả**: 10 người dùng demo với thời gian học
- ✅ **Không Database**: Chạy ngay không cần cài đặt phức tạp
- ✅ **Server Riêng**: Chỉ cho server ID: 1434581250798125068

## 📋 Lệnh Discord

| Lệnh | Mô Tả | GUI |
|------|-------|-----|
| `/trogiup` | Trợ giúp và hướng dẫn | Text |
| `/bangxephang` | Bảng xếp hạng học tập | ✅ Ảnh đẹp |
| `/toi` | Profile cá nhân | Text |
| `/dongho` | Timer pomodoro | Text + Buttons |

## 🎨 Dữ Liệu Demo

```json
[
  {"displayName": "Nguyen Van An", "dayTrackTime": 18600},
  {"displayName": "Tran Thi Mai", "dayTrackTime": 17240},
  {"displayName": "Le Hoang Minh", "dayTrackTime": 16530},
  {"displayName": "Pham Quoc Bao", "dayTrackTime": 15420},
  {"displayName": "Vo Thanh Dat", "dayTrackTime": 14890},
  {"displayName": "Doan Thu Ha", "dayTrackTime": 13750},
  {"displayName": "Bui Tuan Kiet", "dayTrackTime": 12900},
  {"displayName": "Hoang Ngoc Linh", "dayTrackTime": 12180},
  {"displayName": "Dang Minh Quan", "dayTrackTime": 11540},
  {"displayName": "Nguyen Phuong Thao", "dayTrackTime": 10860}
]
```

## 🧪 Test & Kiểm Tra

### Test GUI
```bash
venv/bin/python test_gui_client.py
```

### Test Bot
```bash
venv/bin/python test_simple_bot.py
```

## 📁 Files Quan Trọng

```
StudyLion/
├── simple_vietnamese_bot.py     # Bot chính (sử dụng GUI gốc)
├── run_simple_bot.py            # Script khởi động đơn giản
├── test_gui_client.py           # Test GUI client
├── config/
│   └── secrets.conf             # Token bot
└── src/                         # Code gốc LionBot (cho GUI)
```

## 🔧 Cách Hoạt Động

1. **Bot** (`simple_vietnamese_bot.py`):
   - Kết nối Discord với slash commands
   - Sử dụng dữ liệu giả cố định
   - Gọi GUI client gốc để render ảnh

2. **GUI Server** (gốc):
   - Chạy từ `scripts/start_gui.py`
   - Sử dụng LeaderboardCard gốc
   - Render ảnh với font và layout đẹp

3. **Manager** (`run_simple_bot.py`):
   - Khởi động GUI server trước
   - Khởi động bot sau
   - Theo dõi và cleanup

## 🎯 Kết Quả

### Bảng Xếp Hạng
- 🖼️ **Ảnh đẹp**: Giống hệt GUI gốc của LionBot
- 🏆 **Top 3**: Hiển thị đặc biệt với medal
- 📊 **Thống kê**: Thời gian học theo giờ:phút
- 🇻🇳 **Tiếng Việt**: Server name và text

### Lệnh Khác
- 💬 **Text đẹp**: Embed Discord với màu sắc
- 🎮 **Interactive**: Buttons cho timer
- 📱 **Modern**: Slash commands

## 🎉 Thành Công!

Bot đã hoàn thành với:
- ✅ GUI gốc hoạt động hoàn hảo
- ✅ Render ảnh bảng xếp hạng đẹp
- ✅ Giao diện tiếng Việt
- ✅ Dữ liệu demo phong phú
- ✅ Khởi động đơn giản

**Chạy ngay**: `venv/bin/python run_simple_bot.py` 🚀