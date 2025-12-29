#!/bin/bash
# Script chạy bot ổn định

cd "$(dirname "$0")"

echo "🚀 Khởi động bot..."
source venv/bin/activate

# Chạy bot với nohup
nohup python leaderboard_only_bot.py > logs/bot.log 2>&1 &

BOT_PID=$!
echo "✅ Bot đã khởi động với PID: $BOT_PID"
echo $BOT_PID > logs/bot.pid

echo "📋 Xem log: tail -f logs/bot.log"
echo "🛑 Dừng bot: kill \$(cat logs/bot.pid)"
