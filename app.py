"""
نقطه ورود اصلی پروژه.
این فایل روی PythonAnywhere به عنوان WSGI app اجرا میشه (دقیقا مثل فلسک قبلیت).

نکته فنی: python-telegram-bot v21 به صورت async کار می‌کنه، ولی PythonAnywhere
یه محیط WSGI سینک هست. برای همین یه event loop واحد می‌سازیم و هر webhook
request رو روی همون loop پردازش می‌کنیم. برای حجم ترافیک یه ربات شخصی
کاملا کافیه.
"""
import asyncio
import logging

from flask import Flask, request

from telegram import Update

from config import WEBHOOK_URL
from bot.telegram_app import build_application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

telegram_app = build_application()

# یه event loop واحد برای کل عمر پروسه می‌سازیم
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(telegram_app.initialize())


@app.route("/webhook", methods=["POST"])
def webhook():
    """تلگرام هر پیام جدید رو با POST اینجا میفرسته."""
    try:
        update_data = request.get_json(force=True)
        update = Update.de_json(update_data, telegram_app.bot)
        loop.run_until_complete(telegram_app.process_update(update))
    except Exception:
        logger.exception("خطا در پردازش webhook")
    return "OK"


@app.route("/set_webhook", methods=["GET"])
def set_webhook():
    """
    این route رو فقط یه بار دستی صدا بزن تا به تلگرام بگی آدرس webhook چیه.
    مثال: https://yourusername.pythonanywhere.com/set_webhook
    """
    success = loop.run_until_complete(telegram_app.bot.set_webhook(url=WEBHOOK_URL))
    return {"webhook_set": success, "url": WEBHOOK_URL}


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # فقط برای تست لوکال - روی PythonAnywhere این بخش اجرا نمیشه
    app.run(debug=True, port=5000)
