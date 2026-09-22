# دستیار هوشمند تلگرام (در حال ساخت)

ربات تلگرامی متصل به Google Gemini که متن، عکس، ویدیو و PDF رو می‌فهمه.

## وضعیت فعلی
✅ مرحله ۱: اسکلت پایه ربات
✅ مرحله ۲: اتصال به Gemini API (متن + عکس + ویدیو + PDF)
⬜ مرحله ۳: حافظه بلندمدت (ذخیره مکالمات تو دیتابیس)
⬜ مرحله ۴: سیستم یادآوری زمان‌بندی‌شده
⬜ مرحله ۵: بهبود دیپلوی و مانیتورینگ

## قابلیت‌های فعلی
- 💬 پاسخ به پیام‌های متنی
- 🖼️ تحلیل و توصیف عکس
- 🎬 تحلیل ویدیو
- 📄 خلاصه‌سازی فایل PDF
- ⚠️ محدودیت: فایل‌ها باید کمتر از ۱۵ مگابایت باشن

## ساختار پروژه
```
telegram-assistant/
├── app.py                 # Flask app + webhook endpoint
├── config.py               # تنظیمات مرکزی (از .env می‌خونه)
├── bot/
│   ├── handlers.py         # منطق پاسخ به پیام‌ها/عکس/ویدیو/PDF
│   ├── telegram_app.py     # ساخت Application و ثبت هندلرها
│   └── ai_service.py       # اتصال به Gemini API
├── requirements.txt
└── .env.example
```

## چرا Gemini؟
از Google Gemini API استفاده شده چون:
- کاملاً رایگانه (بدون نیاز به کارت اعتباری)
- دامنه‌ش (`googleapis.com`) تو وایت‌لیست اکانت‌های رایگان PythonAnywhere هست
  (بر خلاف بعضی سرویس‌های دیگه مثل OpenRouter که وایت‌لیست نیستن)
- چندوجهیه (multimodal) - متن، عکس، ویدیو و PDF رو می‌فهمه

## نصب و اجرا (لوکال - فقط برای تست منطق)

```bash
python -m venv venv
source venv/bin/activate  # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env رو باز کن و مقادیر واقعی رو جایگزین کن
```

⚠️ توجه: چون این نسخه با **webhook** کار می‌کنه نه polling، برای تست کامل لوکال
باید با ابزاری مثل [ngrok](https://ngrok.com) یه آدرس عمومی موقت بسازی.

## دیپلوی روی PythonAnywhere

1. کد رو آپلود کن (یا از گیت‌هاب کلون کن تو Bash console)
2. یه virtualenv بساز: `mkvirtualenv --python=/usr/bin/python3.12 botenv`
3. `pip install -r requirements.txt` بزن
4. تو تب **Web**:
   - Source code رو به پوشه پروژه ست کن
   - Virtualenv رو به مسیر virtualenv‌ت ست کن
   - فایل WSGI رو باز کن و محتواش رو با این جایگزین کن:
     ```python
     import sys
     path = '/home/یوزرنیمت/telegram-assistant'
     if path not in sys.path:
         sys.path.append(path)

     from app import app as application
     ```
5. یه فایل `.env` واقعی (نه `.env.example`) تو ریشه پروژه بساز و مقادیر واقعی رو بذار
6. **Reload** بزن
7. یه بار آدرس `https://یوزرنیمت.pythonanywhere.com/set_webhook` رو باز کن
8. تو تلگرام به ربات پیام بده

## کلیدها رو از کجا بگیرم؟

- **توکن تلگرام**: از [@BotFather](https://t.me/BotFather) با دستور `/newbot`
- **کلید Gemini**: از [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

## نکته امنیتی
هیچ‌وقت `.env` یا توکن‌ها رو commit نکن. فایل `.gitignore` از قبل این مورد رو پوشش می‌ده.
اگه یه توکن یا کلید API رو جایی (حتی به‌اشتباه) به اشتراک گذاشتی، همیشه Revoke/Regenerate‌ش کن.
