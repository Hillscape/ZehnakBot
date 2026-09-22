"""
تنظیمات مرکزی پروژه.
همه‌ی متغیرهای محیطی از اینجا خونده میشن، هیچ جای دیگه‌ای مستقیم os.environ صدا نزن.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# مسیر رو صریح می‌دیم چون تو محیط WSGI گاهی load_dotenv() بدون مسیر
# فایل .env رو پیدا نمی‌کنه (working directory متفاوته)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///bot.db")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN تنظیم نشده. فایل .env.example رو کپی کن به .env و پر کن."
    )
