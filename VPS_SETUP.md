# Hướng dẫn Cấu hình VPS cho StudyLion Bot

Tài liệu này hướng dẫn chi tiết các bước để cài đặt và chạy bot StudyLion trên một VPS mới (hệ điều hành Ubuntu/Debian).

## 1. Cập nhật hệ thống và cài đặt công cụ cơ bản

Đầu tiên, hãy SSH vào VPS của bạn và cập nhật các gói phần mềm:

```bash
sudo apt update && sudo apt upgrade -y
```

Cài đặt các công cụ cần thiết (git, python, pip, venv):

```bash
sudo apt install -y git python3 python3-pip python3-venv
```

Cài đặt Node.js và NPM (để chạy PM2):

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

Cài đặt PM2 (Process Manager để giữ bot bot luôn chạy):

```bash
sudo npm install -g pm2
```

## 2. Tải mã nguồn (Source Code)

Bạn có thể clone từ git hoặc upload code từ máy tính lên.

**Cách 1: Clone từ Git (Khuyên dùng)**
Nếu bạn có repo git:
```bash
git clone <link-repo-cua-ban> StudyLion
cd StudyLion
```

**Cách 2: Upload thủ công**
Sử dụng FTP/SFTP để upload folder `StudyLion` lên VPS, sau đó di chuyển vào thư mục:
```bash
cd StudyLion
```

## 3. Cài đặt Môi trường Python (Virtual Environment)

Tạo môi trường ảo (venv) để cách ly thư viện:

```bash
python3 -m venv venv
```

Kích hoạt môi trường ảo:

```bash
source venv/bin/activate
```

Cài đặt các thư viện yêu cầu:

```bash
pip install -r requirements.txt
```

*Lưu ý: Nếu gặp lỗi thiếu thư viện hệ thống khi cài `psycopg` hoặc `pillow`, hãy chạy lệnh sau:*
```bash
sudo apt install -y libpq-dev python3-dev
```

## 4. Cấu hình Bot

Bạn cần tạo các file cấu hình trong thư mục `config/`. Quan trọng nhất là `secrets.conf`.

Tạo file `config/secrets.conf`:
```bash
nano config/secrets.conf
```

Dán nội dung sau vào (thay thế bằng token thật của bạn):

```ini
[STUDYLION]
token = YOUR_DISCORD_BOT_TOKEN_HERE
```
*Nhấn Ctrl+O, Enter để lưu và Ctrl+X để thoát.*

Đảm bảo các file config khác (`bot.conf`, `gui.conf`, v.v.) cũng đã có mặt trong thư mục `config/`.

## 5. Chạy Bot với PM2

File `ecosystem.config.js` đã được cấu hình sẵn để sử dụng interpreter trong `venv`. Bạn chỉ cần khởi động nó:

```bash
pm2 start ecosystem.config.js
```

**Các lệnh PM2 hữu ích:**
- Xem danh sách process: `pm2 list`
- Xem log: `pm2 logs`
- Theo dõi tài nguyên: `pm2 monit`
- Khởi động lại: `pm2 restart studylion`
- Dừng bot: `pm2 stop studylion`

## 6. Cấu hình Tự khởi động (Startup)

Để bot tự chạy lại khi VPS khởi động lại:

```bash
pm2 save
pm2 startup
```
*(Copy và chạy dòng lệnh mà `pm2 startup` in ra màn hình)*

## 7. Troubleshooting (Xử lý lỗi)

- **Lỗi permission**: Nếu báo lỗi quyền truy cập, hãy kiểm tra `chmod +x start.py` hoặc quyền của thư mục.
- **Lỗi venv**: Đảm bảo đường dẫn `interpreter: "./venv/bin/python"` trong `ecosystem.config.js` là chính xác.
- **Xem log chi tiết**: Nếu bot không chạy, kiểm tra file `logs/bot_debug.log` hoặc `error.log`.
