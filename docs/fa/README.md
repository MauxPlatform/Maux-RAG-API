# 🚀 راهنمای استفاده از RAG API

سلام! 👋
به راهنمای استفاده از RAG API خوش اومدید. این API به شما کمک میکنه تا به راحتی یک سیستم پرسش و پاسخ هوشمند با استفاده از اسناد خودتون بسازید.

## 📝 فهرست مطالب
- [شروع سریع](#شروع-سریع)
- [تنظیمات](#تنظیمات)
- [افزودن اسناد](#افزودن-اسناد)
- [پرسش و پاسخ](#پرسش-و-پاسخ)
- [پشتیبانی از AvalAI](#پشتیبانی-از-avalai)

## 🚀 شروع سریع

1. اول پروژه رو کلون کنید:
```bash
git clone https://github.com/MauxPlatform/Maux-RAG-API.git
cd Maux-RAG-API
```

2. پکیج‌های مورد نیاز رو نصب کنید:
```bash
pip install -r requirements.txt
```

3. یک فایل `.env` بسازید و تنظیمات رو وارد کنید:
```env
# برای استفاده از OpenAI
PROVIDER=openai
OPENAI_API_KEY=your_openai_key

# یا برای استفاده از AvalAI
PROVIDER=avalai
AVALAI_API_KEY=your_avalai_key
```

4. سرور رو اجرا کنید:
```bash
uvicorn app.main:app --reload
```

تبریک! 🎉 حالا API شما روی آدرس `http://localhost:8000` در دسترسه.

## ⚙️ تنظیمات

شما می‌تونید از دو سرویس برای هوش مصنوعی استفاده کنید:

### OpenAI
```env
PROVIDER=openai
OPENAI_API_KEY=your_openai_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
```

### AvalAI
```env
PROVIDER=avalai
AVALAI_API_KEY=your_avalai_key
AVALAI_BASE_URL=https://api.avalapis.ir/v1
```

## 📚 افزودن اسناد

برای افزودن اسناد به پایگاه داده، می‌تونید از API یا اسکریپت نمونه استفاده کنید:

### با استفاده از API
```python
import requests

doc = {
    "text": "متن سند شما",
    "metadata": {
        "source": "منبع",
        "date": "2024-01",
        "type": "نوع سند",
        "language": "fa"
    }
}

response = requests.post(
    "http://localhost:8000/v1/vector_db/add_document", 
    json=doc
)
print(response.json())
```

### با استفاده از اسکریپت نمونه
از فایل `examples/add_content.py` می‌تونید برای افزودن اسناد نمونه استفاده کنید:
```bash
python examples/add_content.py
```

## 💬 پرسش و پاسخ

برای پرسش و دریافت پاسخ، می‌تونید از API استفاده کنید:

```python
import requests

chat_request = {
    "model": "gpt-4o-mini",  # یا مدل دلخواه دیگه
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

### پاسخ‌های استریم (زنده)
برای دریافت پاسخ به صورت زنده:

```python
chat_request["stream"] = True
response = requests.post(
    "http://localhost:8000/v1/chat/completions",
    json=chat_request,
    stream=True
)

for line in response.iter_lines():
    if line:
        print(line.decode())
```

## 🌟 پشتیبانی از AvalAI

[AvalAI](https://avalai.ir) یک سرویس ایرانی هوش مصنوعیه که API سازگار با OpenAI ارائه میده. برای استفاده از AvalAI:

1. یک اکانت در [AvalAI](https://avalai.ir) بسازید
2. API key رو از پنل کاربری دریافت کنید
3. تنظیمات رو در فایل `.env` به این شکل تغییر بدید:
```env
PROVIDER=avalai
AVALAI_API_KEY=your_avalai_key
```

همین! 🎉 حالا سیستم به جای OpenAI از AvalAI استفاده می‌کنه.

## 🔍 جستجوی اسناد

برای جستجوی مستقیم در اسناد:

```python
import requests

query = {
    "prompt": "متن جستجوی شما"
}

response = requests.post(
    "http://localhost:8000/v1/vector_db/search_documents",
    json=query
)
print(response.json())
```

## 🧹 پاکسازی پایگاه داده

اگه خواستید همه اسناد رو پاک کنید:

```python
requests.delete("http://localhost:8000/v1/vector_db/clear_collection")
```

## 💡 نکات مفید

1. اسناد رو با متادیتای مناسب ذخیره کنید تا بعداً راحت‌تر پیداشون کنید
2. از استریمینگ برای پاسخ‌های طولانی استفاده کنید
3. می‌تونید بین OpenAI و AvalAI به راحتی سوییچ کنید
4. اسناد فارسی رو با `language: "fa"` در متادیتا مشخص کنید

## 🤔 سوالات متداول

### چطور می‌تونم مدل رو عوض کنم؟
در فایل `.env` می‌تونید `CHAT_MODEL` رو تغییر بدید یا موقع درخواست در پارامتر `model` مدل دلخواه رو مشخص کنید.


### سیستم چطور کار می‌کنه؟
1. اسناد شما به vector تبدیل و ذخیره میشن
2. موقع پرسش، متن سوال هم به vector تبدیل میشه
3. شبیه‌ترین اسناد به سوال پیدا میشن
4. این اسناد همراه با سوال به model هوش مصنوعی داده میشن
5. model با استفاده از این اطلاعات پاسخ میده

