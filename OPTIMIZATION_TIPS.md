# Các Mẹo Tối Ưu StudyLion trên VPS Yếu

Ngoài việc restart định kỳ, bạn nên áp dụng các cài đặt sau để bot chạy nhẹ nhàng hơn.

## 1. Giới hạn RAM và Restart Delay (Đã tự động cấu hình)

Mình đã cập nhật file `ecosystem.config.js` để thêm:
- **Max Memory**: 200MB. Nếu bot ngốn quá 200MB RAM, nó sẽ tự động restart để giải phóng bộ nhớ.
- **Restart Delay**: 5 giây. Nếu bot crash, nó sẽ đợi 5s mới chạy lại, tránh spam CPU liên tục.

## 2. Giảm số lượng Process xử lý ảnh (Cần làm thủ công)

Mặc định bot có thể chạy nhiều process để render ảnh nhanh hơn, nhưng sẽ tốn RAM. Trên VPS yếu (1GB RAM), bạn nên giảm xuống 1.

Mở file `config/gui.conf`:
```bash
nano config/gui.conf
```

Tìm và sửa dòng `process_count`:
```ini
[GUI]
process_count = 1
```

## 3. Swap Memory (Bộ nhớ ảo)

Nếu VPS quá ít RAM, hãy tạo Swap để tránh bị crash do hết RAM.

```bash
# Tạo 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

## 4. Áp dụng thay đổi

Sau khi sửa config, hãy chạy:
```bash
pm2 restart studylion
```
