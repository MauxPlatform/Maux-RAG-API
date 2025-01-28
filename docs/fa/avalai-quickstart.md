# 🚀 راهنمای سریع استفاده از AvalAI

سلام! 👋
این راهنما به شما کمک می‌کنه تا سریعاً سیستم RAG رو با [AvalAI](https://avalai.ir) راه‌اندازی کنید.

## 📋 پیش‌نیازها

1. پایتون 3.8 یا بالاتر
2. یک اکانت در [AvalAI](https://avalai.ir)
3. API key از پنل کاربری AvalAI

## 🚀 شروع سریع

1. **نصب و راه‌اندازی**
```bash
# کلون کردن پروژه
git clone https://github.com/MauxPlatform/Maux-RAG-API.git
cd Maux-RAG-API

# نصب پکیج‌ها
pip install -r requirements.txt
```

2. **تنظیمات AvalAI**

یک فایل `.env` بسازید:
```env
PROVIDER=avalai
AVALAI_API_KEY=your_avalai_key
AVALAI_BASE_URL=https://api.avalapis.ir/v1
CHAT_MODEL=gpt-4o-mini
```

3. **اجرای سرور**
```bash
uvicorn app.main:app --reload
```

## 📚 افزودن اسناد نمونه

برای تست سریع سیستم، می‌تونید از اسکریپت نمونه استفاده کنید:
```bash
python examples/add_content.py
```

این اسکریپت چند سند نمونه فارسی به سیستم اضافه می‌کنه.

## 💬 تست سیستم

1. **افزودن یک سند جدید**
```python
import requests

doc = {
    "text": "این یک متن تست است برای سیستم RAG با استفاده از AvalAI",
    "metadata": {
        "source": "تست",
        "language": "fa"
    }
}

response = requests.post(
    "http://localhost:8000/v1/vector_db/add_document",
    json=doc
)
print(response.json())
```

2. **پرسش و پاسخ**
```python
chat_request = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": "سوال شما اینجا"
        }
    ]
}

response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json=chat_request
)
print(response.json())
```

## 🔄 تغییر مدل‌ها

AvalAI مدل‌های مختلفی ارائه میده. برای تغییر مدل می‌تونید:

1. در فایل `.env`:
```env
CHAT_MODEL=gpt-4o-mini  # یا هر مدل دیگه
```

2. یا موقع درخواست:
```python
chat_request = {
    "model": "مدل دلخواه شما",
    "messages": [...]
}
```

## 💡 نکات مهم

1. **محدودیت‌های API**
   - به محدودیت‌های API در پنل AvalAI توجه کنید
   - از Rate Limiting آگاه باشید

2. **بهینه‌سازی هزینه**
   - از استریمینگ برای پاسخ‌های طولانی استفاده کنید
   - اسناد رو با متادیتای مناسب ذخیره کنید

3. **زبان فارسی**
   - حتماً `language: "fa"` رو در متادیتا مشخص کنید
   - از یونیکد درست برای متون فارسی استفاده کنید

## 🆘 عیب‌یابی

### خطای اعتبارسنجی API
```
ValueError: AVALAI_API_KEY is required when using AvalAI provider
```
- مطمئن شید `AVALAI_API_KEY` در فایل `.env` تنظیم شده
- درستی API key رو چک کنید

### خطای اتصال
```
ConnectionError: Could not connect to AvalAI
```
- اتصال اینترنت رو چک کنید
- VPN یا پروکسی رو چک کنید
- درستی `AVALAI_BASE_URL` رو بررسی کنید


