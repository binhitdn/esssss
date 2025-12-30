
import sys
import os
import traceback

print("--- Checking Dependencies ---")

# 1. Check Pillow
try:
    from PIL import Image, ImageDraw, ImageFont
    print("✅ Pillow imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Pillow: {e}")
    sys.exit(1)

# 2. Check Font Loading
print("\n--- Checking Font Loading ---")
font_path = "skins/base/assets/fonts/Inter/Inter-Bold.ttf"
if not os.path.exists(font_path):
    print(f"❌ Font file not found at: {font_path}")
    print("Please check if 'skins' directory is uploaded correctly.")
else:
    try:
        font = ImageFont.truetype(font_path, 40)
        print(f"✅ Font loaded successfully: {font_path}")
    except Exception as e:
        print(f"❌ Failed to load font: {e}")
        print("This usually means missing system libraries like 'libfreetype6-dev'.")

# 3. Check Image Creation
print("\n--- Checking Image Drawing ---")
try:
    img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Test", font=font, fill=(255, 255, 255))
    print("✅ Image created and text drawn successfully")
except Exception as e:
    print(f"❌ Failed to draw image: {e}")

print("\n--- Check Complete ---")
