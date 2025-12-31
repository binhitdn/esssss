# StudyLion Web Dashboard

Trang web thống kê server Discord StudyLion với bảng xếp hạng học tập.

## Tính năng

- 📊 **Dashboard tổng quan**: Thống kê tổng số học viên, thời gian học
- 🏆 **Bảng xếp hạng**: Top 10 học viên theo ngày/tuần/tháng
- 🔄 **Auto refresh**: Tự động cập nhật dữ liệu mỗi 30 giây
- 📱 **Responsive**: Tương thích mobile và desktop
- 🎨 **UI đẹp**: Giao diện hiện đại với gradient và animations

## Cài đặt

### 1. Cài đặt dependencies

```bash
cd web
pip install -r requirements.txt
```

### 2. Chạy web server

```bash
# Cách 1: Chạy trực tiếp
python app.py

# Cách 2: Chạy qua starter script
python start_web.py
```

### 3. Truy cập dashboard

Mở trình duyệt và truy cập: http://localhost:5001

## Cấu trúc

```
web/
├── app.py              # Flask web server chính
├── start_web.py        # Script khởi động
├── requirements.txt    # Dependencies
├── templates/
│   └── dashboard.html  # Template trang chủ
└── README.md          # Tài liệu này
```

## API Endpoints

- `GET /` - Trang dashboard chính
- `GET /api/leaderboard/<period>` - Lấy bảng xếp hạng (day/week/month)
- `GET /api/stats` - Lấy thống kê tổng quan

## Tính năng chính

### Dashboard
- Hiển thị thông tin server
- Thống kê số học viên hoạt động
- Tổng thời gian học tập
- Thời gian server hiện tại

### Bảng xếp hạng
- Top 10 học viên xuất sắc
- Hiển thị theo ngày/tuần/tháng
- Thời gian học được format đẹp (XXh YYm)
- Rank badges với icons đặc biệt cho top 3

### Auto refresh
- Tự động làm mới dữ liệu mỗi 30 giây
- Cache dữ liệu 5 phút để tránh spam API
- Button refresh thủ công

## Cấu hình

Các cấu hình chính trong `app.py`:

```python
API_BASE_URL = "https://api.14study.io.vn/api/leaderboard/top-learners"
CACHE_DURATION = 300  # 5 phút
PORT = 5001
```

## Troubleshooting

### Lỗi không kết nối được API
- Kiểm tra API endpoint có hoạt động không
- Kiểm tra kết nối internet
- Xem log trong terminal

### Lỗi Flask không khởi động
- Đảm bảo đã cài đặt dependencies: `pip install -r requirements.txt`
- Kiểm tra port 5001 có bị chiếm không
- Chạy với Python 3.7+

### Dữ liệu không hiển thị
- Kiểm tra API trả về dữ liệu hợp lệ
- Xem console browser để debug JavaScript
- Kiểm tra network tab trong DevTools