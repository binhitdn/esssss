# Bot Bảng Xếp Hạng - Phiên Bản Tối Giản

## 🎯 **CHỈ CÓ BẢNG XẾP HẠNG**

Bot đã được làm sạch, chỉ giữ lại chức năng bảng xếp hạng duy nhất.

## 🚀 **Khởi Động**

```bash
# Khởi động bot (cách duy nhất)
venv/bin/python run_leaderboard_bot.py
```

## 🏆 **Chức Năng Duy Nhất**

| Lệnh | Mô Tả | Tính Năng |
|------|-------|-----------|
| `/bangxephang` | Bảng xếp hạng học tập | ✅ Ảnh đẹp với GUI gốc |

**Đã xóa:**
- ❌ `/trogiup` - Trợ giúp
- ❌ `/toi` - Profile cá nhân  
- ❌ `/dongho` - Timer pomodoro

## 📁 **Files Còn Lại**

### **Cần thiết:**
```
StudyLion/
├── leaderboard_only_bot.py     # Bot chính (chỉ bảng xếp hạng)
├── run_leaderboard_bot.py      # Script khởi động
├── config/secrets.conf         # Token bot
└── src/                        # LionBot gốc (cho GUI)
```

### **Đã xóa:**
- ❌ `simple_vietnamese_bot.py` (bot cũ với nhiều chức năng)
- ❌ `run_simple_bot.py` (script cũ)
- ❌ `start_simple_bot.py` (script cũ)
- ❌ `test_simple_bot.py` (test cũ)
- ❌ `debug_bot.py` (debug cũ)
- ❌ `test_format_time.py` (test format)

## 🎨 **Bảng Xếp Hạng**

### **Tính năng:**
- ✅ **Format**: `05h10p00s` (giờ:phút:giây)
- ✅ **Top 3**: In đậm, màu vàng
- ✅ **GUI gốc**: Render ảnh đẹp
- ✅ **Server name**: `14 hours a day(STUDY VIP)`
- ✅ **Kích thước**: Scale 2 (gốc)
- ✅ **Gửi**: Tin nhắn thường (không embed)

### **Dữ liệu demo:**
```
🥇 1ST - Nguyen Van An - 05h10p00s
🥈 2ND - Tran Thi Mai - 04h47p20s  
🥉 3RD - Le Hoang Minh - 04h35p30s
4. Pham Quoc Bao - 04h17p00s
5. Vo Thanh Dat - 04h08p10s
...
```

## 🔧 **Cách Hoạt Động**

### **Bot Class:**
```python
class LeaderboardBot(commands.Bot):
    # Chỉ có setup cho bảng xếp hạng
    # Status: "watching bảng xếp hạng 🏆"
```

### **Command duy nhất:**
```python
@bot.tree.command(name="bangxephang")
async def leaderboard_command(interaction):
    # 1. Respond ngay để tránh timeout
    # 2. Render ảnh qua GUI gốc
    # 3. Gửi ảnh + text trong channel
```

### **Render function:**
```python
async def render_leaderboard_image(data):
    # Sử dụng GUI client gốc
    # Route: 'leaderboard_card'
    # Format: 05h10p00s
```

## 🧪 **Test**

### **Test nhanh:**
```bash
# Kiểm tra bot có chạy không
ps aux | grep leaderboard_only_bot

# Kiểm tra GUI server
ls -la gui.sock
```

### **Test trong Discord:**
```
/bangxephang
```

**Kết quả mong đợi:**
1. Bot: "🎨 Đang tạo bảng xếp hạng..." (ephemeral)
2. Bot: Gửi ảnh + "🏆 **Bảng Xếp Hạng Học Tập**" trong channel

## 🎯 **Tối Ưu Hoàn Toàn**

### **Đã loại bỏ:**
- ❌ Tất cả lệnh không liên quan
- ❌ Tất cả file test/debug cũ
- ❌ Tất cả script khởi động cũ
- ❌ Tất cả chức năng phụ

### **Chỉ giữ lại:**
- ✅ Lệnh `/bangxephang`
- ✅ GUI render gốc
- ✅ Dữ liệu demo 10 người
- ✅ Format `05h10p00s`
- ✅ Server restriction

## 🎉 **HOÀN THÀNH**

Bot bây giờ:
- 🏆 **Chỉ có bảng xếp hạng**
- 🎨 **GUI gốc hoạt động**
- 📊 **Format đẹp `05h10p00s`**
- 🚀 **Khởi động nhanh**
- 🧹 **Code sạch sẽ**

**Chạy ngay**: `venv/bin/python run_leaderboard_bot.py` 🚀