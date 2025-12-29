# StudyLion Private Bot Setup - "14 hours a days"

## Tối ưu hóa cho server riêng (ID: 1434581250798125068)

Bot này được cấu hình đặc biệt cho server **"14 hours a days"** với các tối ưu hóa sau:

### 🔒 Bảo mật Server (Server Restriction)

Bot được cấu hình để **CHỈ** hoạt động trên server ID: `1434581250798125068`

- ✅ Tự động rời khỏi bất kỳ server nào khác
- ✅ Log tất cả các lần join/leave server
- ✅ Đảm bảo bot chỉ phục vụ server riêng của bạn

### 🇻🇳 Ngôn ngữ Tiếng Việt

Bot được cấu hình sử dụng tiếng Việt làm ngôn ngữ mặc định:

- 🔧 Locale mặc định: `vi` (Tiếng Việt)
- ⚠️ **Lưu ý**: Hiện tại chưa có file dịch tiếng Việt trong `locales/`
- 📝 Bot sẽ fallback về tiếng Anh cho đến khi có file dịch
- 💡 Để thêm dịch tiếng Việt: Tạo thư mục `locales/vi/LC_MESSAGES/` và thêm file `.po`

### Các module đã tắt:

- ❌ `sysadmin` - Không cần cho bot private
- ❌ `shop` - Không cần hệ thống shop
- ❌ `sponsors` - Không cần sponsor system  
- ❌ `topgg` - Không cần tích hợp Top.gg
- ❌ `premium` - Không cần tính năng premium
- ❌ `test` - Không cần trong production

### Các dịch vụ đã tắt:

- ❌ IPC Server - Không cần cho single server
- ❌ Analytics Server - Không cần tracking phức tạp
- ❌ Top.gg webhook - Không sử dụng

### Tối ưu hóa:

- 🔧 Giảm log level để tránh spam
- 🔧 Tối ưu text tracking batch time
- 🔧 Hạn chế server theo ID
- 🔧 Cấu hình locale tiếng Việt
- 🔧 Loại bỏ domains không cần thiết

### Khởi động bot:

#### 🎨 Với GUI rendering (khuyên dùng - có leaderboard):
```bash
# Khởi động đầy đủ với GUI server
python scripts/start_private_with_gui.py
```

#### 🤖 Chỉ bot (không có render ảnh):
```bash
# Sử dụng script tối ưu (khuyên dùng)
python scripts/start_leo_private.py

# Hoặc script gốc
python scripts/start_leo.py
```

#### 🧪 Test GUI system:
```bash
# Kiểm tra GUI có hoạt động không
python scripts/test_gui.py
```

### Lỗi thường gặp và cách fix:

1. **IPC Connection Error** - ✅ Đã fix bằng cách tắt IPC
2. **Webhook URL Error** - ✅ Đã tắt premium/topgg modules  
3. **Command.to_dict() Error** - ✅ Đã fix API compatibility
4. **Graphics service unavailable** - ✅ Dùng `start_private_with_gui.py`
5. **Bot joins wrong server** - ✅ Tự động rời khỏi server không được phép

### GUI Rendering:

- 🎨 **Leaderboard images**: Cần GUI server
- 📊 **Statistics charts**: Cần GUI server  
- 🏆 **Achievement cards**: Cần GUI server
- ⏱️ **Timer graphics**: Cần GUI server

### Monitoring:

- Bot sẽ chỉ log các lỗi quan trọng
- GUI server tự động restart nếu crash
- Tất cả processes được monitor và cleanup tự động
- Server restriction được log để tracking

### Biến môi trường (Environment Variables):

Các biến được set tự động bởi startup scripts:

- `STUDYLION_PRIVATE=1` - Bật chế độ private bot
- `STUDYLION_SINGLE_SERVER=1434581250798125068` - Server ID được phép
- `STUDYLION_LOCALE=vi` - Ngôn ngữ tiếng Việt