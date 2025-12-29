#!/bin/bash

# StudyLion Leaderboard Bot Starter
# Chạy toàn bộ project với GUI và Bot

echo "🚀 Khởi động StudyLion Leaderboard Bot"
echo "======================================"

# Kiểm tra virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Không tìm thấy virtual environment!"
    echo "💡 Hãy tạo venv trước: python3 -m venv venv"
    exit 1
fi

# Kiểm tra token
if [ ! -f "config/secrets.conf" ]; then
    echo "❌ Không tìm thấy config/secrets.conf!"
    echo "💡 Tạo file này với nội dung:"
    echo "[STUDYLION]"
    echo "token = your_bot_token_here"
    exit 1
fi

# Kiểm tra token có được cấu hình không
if ! grep -q "token =" config/secrets.conf; then
    echo "❌ Token chưa được cấu hình trong secrets.conf!"
    exit 1
fi

echo "✅ Cấu hình OK"

# Dọn dẹp process cũ
echo "🧹 Dọn dẹp process cũ..."
pkill -f "leaderboard_only_bot.py" 2>/dev/null || true
pkill -f "start_gui.py" 2>/dev/null || true
rm -f gui.sock 2>/dev/null || true

# Khởi động GUI server
echo "🎨 Khởi động GUI server..."
venv/bin/python scripts/start_gui.py &
GUI_PID=$!

# Đợi GUI server khởi động
sleep 3

# Kiểm tra GUI server có chạy không
if ! kill -0 $GUI_PID 2>/dev/null; then
    echo "❌ GUI server không khởi động được!"
    exit 1
fi

echo "✅ GUI server đã khởi động (PID: $GUI_PID)"

# Khởi động bot
echo "🏆 Khởi động leaderboard bot..."
venv/bin/python leaderboard_only_bot.py &
BOT_PID=$!

# Đợi bot khởi động
sleep 2

# Kiểm tra bot có chạy không
if ! kill -0 $BOT_PID 2>/dev/null; then
    echo "❌ Bot không khởi động được!"
    kill $GUI_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Bot đã khởi động (PID: $BOT_PID)"

echo ""
echo "🎉 KHỞI ĐỘNG THÀNH CÔNG!"
echo "======================================"
echo "🏆 Chức năng: Bảng xếp hạng từ API"
echo "🎯 Server: 1434581250798125068"
echo "📊 GUI: ✅ Có"
echo "📡 API: http://192.168.128.173:3001"
echo ""
echo "📋 Lệnh Discord:"
echo "   /bangxephang - Bảng xếp hạng hôm nay"
echo "   /bangxephang-tuan - Bảng xếp hạng tuần này"
echo "   /bangxephang-thang - Bảng xếp hạng tháng này"
echo ""
echo "⌨️ Nhấn Ctrl+C để dừng"
echo "======================================"

# Function để dọn dẹp khi thoát
cleanup() {
    echo ""
    echo "🛑 Đang tắt..."
    
    # Tắt bot
    if kill -0 $BOT_PID 2>/dev/null; then
        kill $BOT_PID
        echo "✅ Đã tắt bot"
    fi
    
    # Tắt GUI
    if kill -0 $GUI_PID 2>/dev/null; then
        kill $GUI_PID
        echo "✅ Đã tắt GUI server"
    fi
    
    # Dọn dẹp
    rm -f gui.sock 2>/dev/null || true
    
    echo "✅ Dọn dẹp hoàn tất"
    exit 0
}

# Bắt signal Ctrl+C
trap cleanup SIGINT SIGTERM

# Theo dõi process
while true; do
    # Kiểm tra bot còn chạy không
    if ! kill -0 $BOT_PID 2>/dev/null; then
        echo "⚠️ Bot đã dừng!"
        cleanup
    fi
    
    # Kiểm tra GUI còn chạy không
    if ! kill -0 $GUI_PID 2>/dev/null; then
        echo "⚠️ GUI server đã dừng!"
        cleanup
    fi
    
    sleep 1
done