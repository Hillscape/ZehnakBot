"""
تنظیمات مرکزی پروژه.
همه‌ی متغیرهای محیطی از اینجا خونده میشن، هیچ جای دیگه‌ای مستقیم os.environ صدا نزن.
"""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///bot.db")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN تنظیم نشده. فایل .env.example رو کپی کن به .env و پر کن."
    )
