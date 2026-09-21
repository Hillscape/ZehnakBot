# دستیار هوشمند تلگرام (در حال ساخت)

ربات تلگرامی با حافظه بلندمدت، یادآوری زمان‌بندی‌شده، و اتصال به Claude API.

## وضعیت فعلی
✅ مرحله ۱: اسکلت پایه ربات (این نسخه)
⬜ مرحله ۲: اتصال به دیتابیس
⬜ مرحله ۳: اتصال به Claude API
⬜ مرحله ۴: حافظه بلندمدت
⬜ مرحله ۵: سیستم یادآوری
⬜ مرحله ۶: دیپلوی نهایی + مانیتورینگ

## ساختار پروژه
```
telegram-assistant/
├── app.py              # Flask app + webhook endpoint
├── config.py           # تنظیمات مرکزی (از .env می‌خونه)
├── bot/
│   ├── handlers.py      # منطق پاسخ به پیام‌ها
│   └── telegram_app.py  # ساخت Application و ثبت هندلرها
├── requirements.txt
└── .env.example
```

## نصب و اجرا (لوکال - فقط برای تست منطق)

```bash
python -m venv venv
source venv/bin/activate  # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env رو باز کن و TELEGRAM_BOT_TOKEN رو پر کن
```

⚠️ توجه: چون این نسخه با **webhook** کار می‌کنه نه polling، برای تست کامل لوکال
باید با ابزاری مثل [ngrok](https://ngrok.com) یه آدرس عمومی موقت بسازی و تو
`WEBHOOK_URL` بذاریش. برای دیپلوی نهایی مستقیم می‌ریم سراغ PythonAnywhere.

## دیپلوی روی PythonAnywhere

1. کد رو آپلود کن (یا از گیت‌هاب کلون کن تو Bash console)
2. یه virtualenv بساز و `pip install -r requirements.txt` بزن
3. تو تب **Web**، فایل WSGI رو طوری تنظیم کن که از `app.py` همون `app` رو ایمپورت کنه:
   ```python
   from app import app as application
   ```
4. متغیرهای محیطی رو یا تو فایل `.env` روی سرور بذار، یا تو تنظیمات WSGI ست کن
5. بعد از ریستارت وب‌اپ، یه بار آدرس `https://یوزرنیم.pythonanywhere.com/set_webhook`
   رو تو مرورگر باز کن تا webhook به تلگرام معرفی بشه
6. تست کن: تو تلگرام به ربات پیام بده

## دستور ساخت ربات تو BotFather
1. تو تلگرام برو سراغ [@BotFather](https://t.me/BotFather)
2. `/newbot` بزن و اسم و یوزرنیم انتخاب کن
3. توکنی که میده رو بذار تو `.env`

## نکته امنیتی
هیچ‌وقت `.env` یا توکن‌ها رو commit نکن. فایل `.gitignore` از قبل این مورد رو پوشش می‌ده.
