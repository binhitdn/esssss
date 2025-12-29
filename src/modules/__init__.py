this_package = 'modules'

# Chỉ giữ lại 3 modules chính và dependencies cần thiết
active = [
    '.config',        # Cần thiết cho cấu hình
    '.user_config',   # Cần thiết cho user settings
    '.skins',         # Cần thiết cho UI ảnh
    '.ranks',         # ✓ Module chính: Bảng xếp hạng
    '.statistics',    # ✓ Module chính: Thống kê học tập
    '.pomodoro',      # ✓ Module chính: Pomodoro timer
]


async def setup(bot):
    for ext in active:
        await bot.load_extension(ext, package=this_package)
