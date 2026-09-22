# 🤖 Telegram AI Assistant

ربات تلگرامی هوشمند و چندوجهی (multimodal) که با Google Gemini کار می‌کنه — متن، عکس، ویدیو و PDF رو می‌فهمه و بهشون جواب می‌ده.

## ✨ ویژگی‌ها

| قابلیت | توضیح |
|---|---|
| 💬 گفتگوی متنی | پاسخ‌گویی هوشمند به پیام‌های متنی فارسی |
| 🖼️ تحلیل عکس | توصیف تصویر یا پاسخ به سوال درباره‌ش |
| 🎬 تحلیل ویدیو | فهم محتوای ویدیو و توضیح اون |
| 📄 خلاصه‌سازی PDF | استخراج نکات مهم از فایل‌های PDF |
| ⚡ Webhook-based | بدون نیاز به polling یا پروسه همیشه-روشن |

## 🏗️ معماری

```
تلگرام → Webhook (POST) → Flask App → python-telegram-bot → Gemini API
                                                                    │
                                                          متن / عکس / ویدیو / PDF
```

ربات به‌جای **polling** (که نیاز به یه پروسه دائمی داره)، از **webhook** استفاده می‌کنه:
تلگرام مستقیماً هر پیام جدید رو با یه درخواست HTTP به سرور Flask می‌فرسته. این باعث میشه
بشه ربات رو روی هاستینگ‌های رایگان و بدون پشتیبانی از background process (مثل PythonAnywhere Free Tier) هم اجرا کرد.

## 🛠️ تکنولوژی‌ها

- **Python 3.12**
- **python-telegram-bot v21** — فریم‌ورک ربات (async)
- **Flask** — سرور webhook
- **Google Gemini API** (`gemini-3.5-flash-lite`) — موتور هوش مصنوعی چندوجهی
- **httpx** — کلاینت HTTP async برای اتصال به Gemini
- **python-dotenv** — مدیریت متغیرهای محیطی

## 📁 ساختار پروژه

```
telegram-assistant/
├── app.py                 # Flask app + webhook endpoint (نقطه ورود)
├── config.py               # تنظیمات مرکزی، خواندن از .env
├── bot/
│   ├── handlers.py         # منطق پاسخ به متن/عکس/ویدیو/PDF
│   ├── telegram_app.py     # ساخت Application و ثبت هندلرها
│   └── ai_service.py       # لایه اتصال به Gemini API
├── requirements.txt
├── .env.example             # الگوی متغیرهای محیطی مورد نیاز
└── .gitignore
```

## 🚀 راه‌اندازی

### پیش‌نیازها
- یه توکن ربات تلگرام از [@BotFather](https://t.me/BotFather)
- یه کلید API رایگان از [Google AI Studio](https://aistudio.google.com/apikey)

### نصب

```bash
git clone <آدرس-ریپو>
cd telegram-assistant
python -m venv venv
source venv/bin/activate   # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env رو باز کن و مقادیر واقعی رو جایگزین کن
```

### متغیرهای محیطی (`.env`)

| متغیر | توضیح |
|---|---|
| `TELEGRAM_BOT_TOKEN` | توکن ربات از BotFather |
| `WEBHOOK_URL` | آدرس عمومی که تلگرام بهش پیام میفرسته (مثلاً `https://domain.com/webhook`) |
| `GEMINI_API_KEY` | کلید API از Google AI Studio |
| `DATABASE_URL` | مسیر دیتابیس (پیش‌فرض: SQLite محلی) |

### اجرا (لوکال، برای تست)

چون این پروژه با webhook کار می‌کنه نه polling، برای تست لوکال به یه آدرس عمومی موقت نیاز داری (مثلاً با [ngrok](https://ngrok.com)):

```bash
python app.py
```

### دیپلوی (PythonAnywhere یا هر هاست دیگه‌ای که WSGI پشتیبانی کنه)

1. کد و `.env` رو روی سرور قرار بده
2. `pip install -r requirements.txt` بزن
3. فایل WSGI سرور رو طوری تنظیم کن که `app` رو از `app.py` ایمپورت کنه:
   ```python
   from app import app as application
   ```
4. بعد از reload کردن اپ، یه بار آدرس `/set_webhook` رو باز کن تا webhook به تلگرام معرفی بشه

## 🧠 چند تصمیم فنی و چرایی‌شون

**چرا Gemini و نه یه مدل دیگه؟**
Gemini API واقعاً رایگانه (نه فقط یه دوره تست محدود) و دامنه‌ش (`googleapis.com`) روی
وایت‌لیست اکانت‌های رایگان PythonAnywhere هم هست — برخلاف بعضی سرویس‌های واسط مثل OpenRouter
که با خطای دسترسی مواجه میشن چون تو اون وایت‌لیست نیستن.

**چرا webhook به‌جای polling؟**
Polling نیاز به یه پروسه که دائم در حال اجراست داره (`run_polling()`)، ولی هاست‌های
رایگان معمولاً همچین قابلیتی (Always-on tasks) رو ساپورت نمی‌کنن. با webhook، سرور فقط
وقتی پیامی میاد بیدار میشه — سازگار با محیط‌های serverless/shared hosting.

**چرا فایل‌ها inline (base64) فرستاده میشن نه از طریق File API؟**
برای فایل‌های کوچیک (زیر ۱۵ مگابایت که محدودیت این پروژه‌ست) ارسال inline ساده‌تره و
یه round-trip اضافه (آپلود جدا) نیاز نداره. برای فایل‌های بزرگ‌تر، مرحله بعدی توسعه
می‌تونه از Gemini File API استفاده کنه.

## 🗺️ قدم‌های بعدی

- [ ] حافظه بلندمدت (ذخیره تاریخچه مکالمات در دیتابیس)
- [ ] سیستم یادآوری زمان‌بندی‌شده (APScheduler)
- [ ] پشتیبانی از فایل‌های بزرگ‌تر با Gemini File API
- [ ] Rate limiting برای جلوگیری از سو‌استفاده

## 🔒 امنیت

- تمام کلیدها و توکن‌ها فقط در `.env` نگه‌داری میشن (که در `.gitignore` هست و هرگز commit نمیشه)
- هیچ کلید یا توکنی به‌صورت hardcoded در کد وجود نداره
