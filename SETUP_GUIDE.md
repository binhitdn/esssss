# Hướng Dẫn Khởi Động Bot Sau Khi Tối Giản Hóa

## Vấn đề gặp phải

Bot thiếu dependencies trong virtual environment. Cần cài đặt lại các thư viện cần thiết.

## Các bước khắc phục

### 1. Kích hoạt virtual environment

```bash
cd /Users/binh/StudyLion
source venv/bin/activate
```

### 2. Cài đặt lại dependencies

```bash
pip install -r requirements.txt
```

Nếu gặp lỗi với `psycopg`, thử:

```bash
pip install --upgrade psycopg[pool]
```

### 3. Khởi động bot

```bash
python3 scripts/start_simple.py
```

Hoặc sử dụng script cũ:

```bash
python3 scripts/start_leo_private.py
```

## Lưu ý

- Đảm bảo PostgreSQL database đang chạy
- Kiểm tra file config có đúng thông tin database không
- Bot cần TOKEN trong file config để kết nối Discord

## Nếu vẫn gặp lỗi

Thử cài đặt từng package quan trọng:

```bash
pip install aiohttp discord.py psycopg[pool] pillow cachetools
```
