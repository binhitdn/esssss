# Tự động restart bot định kỳ

Để đảm bảo bot luôn hoạt động ổn định và tránh lỗi "treo" sau thời gian dài, bạn nên cấu hình cho PM2 tự động restart bot định kỳ (ví dụ: mỗi 6 tiếng một lần).

## Cách 1: Sử dụng tính năng cron của PM2 (Khuyên dùng)

Chạy lệnh sau trên VPS:

```bash
# Restart app "studylion" vào phút thứ 39 của mỗi giờ
pm2 restart studylion --cron "39 * * * *"
```

Để lưu lại cấu hình này (để khi reboot VPS vẫn giữ nguyên):
```bash
pm2 save
```

## Cách 2: Sử dụng script restart

Nếu cách trên không hiệu quả, bạn có thể dùng script này.

1. Tạo file `restart_services.sh`:

```bash
cat > restart_services.sh << 'EOF'
#!/bin/bash
export PATH=$PATH:/usr/bin:/usr/local/bin

echo "[$(date)] Restarting StudyLion services..."
pm2 restart studylion
echo "[$(date)] Done."
EOF
```

2. Cấp quyền chạy:
```bash
chmod +x restart_services.sh
```

3. Thêm vào crontab (`crontab -e`):
```
0 */6 * * * /root/esssss/restart_services.sh >> /root/esssss/logs/restart.log 2>&1
```

## Lưu ý

Việc restart này chỉ tốn vài giây và sẽ giải phóng hoàn toàn RAM/CPU bị kẹt, giúp bot chạy mượt như mới.
