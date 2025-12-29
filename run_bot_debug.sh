#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
exec python leaderboard_only_bot.py
