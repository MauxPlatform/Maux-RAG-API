# In this example, we initialize the vector database and add documents to it
import requests
from typing import Dict, List
import json

BASE_URL = "http://localhost:8000/v1"

def initialize_collection():
    """Initialize the vector database collection"""
    response = requests.post(f"{BASE_URL}/vector_db/initialize_collection")
    print("Collection initialization status:", response.json())

def add_documents():
    """Add sample Persian documents to the collection"""
    docs = [
        {
            "text": "شرکت ماکس در سه‌ماهه چهارم سال ۲۰۲۳ به درآمد ۱۲.۵ میلیون دلار دست یافت که رشد ۴۵ درصدی نسبت به سال قبل را نشان می‌دهد. عوامل اصلی این رشد شامل اشتراک‌های پلتفرم هوش مصنوعی و مشارکت‌های سازمانی بود. حاشیه سود عملیاتی به ۲۸ درصد بهبود یافت.",
            "metadata": {
                "source": "گزارش_مالی",
                "date": "2023-Q4",
                "type": "درآمد",
                "language": "fa"
            }
        },
        {
            "text": "معرفی محصولات شرکت ماکس: پلتفرم هوش مصنوعی ما راهکارهای سازمانی شامل مدل‌های زبانی، سیستم‌های RAG و راه‌حل‌های سفارشی هوش مصنوعی ارائه می‌دهد. قیمت‌گذاری فعلی از ۴۹۹ دلار در ماه برای سطح تجاری و ۴،۹۹۹ دلار در ماه برای مشتریان سازمانی شروع می‌شود.",
            "metadata": {
                "source": "مستندات_محصول",
                "date": "2024-01",
                "type": "محصول",
                "language": "fa"
            }
        },
        {
            "text": "پروفایل شرکت ماکس: تاسیس شده در سال ۲۰۲۲، دفتر مرکزی در سانفرانسیسکو با دفاتر در دبی و لندن. تعداد کارمندان: ۸۵ نفر (از ژانویه ۲۰۲۴). تمرکز اصلی بر راه‌حل‌های هوش مصنوعی سازمانی و مدل‌های زبانی سفارشی.",
            "metadata": {
                "source": "اطلاعات_شرکت",
                "date": "2024-01",
                "type": "شرکت",
                "language": "fa"
            }
        },
        {
            "text": "معیارهای رشد ماکس در سال ۲۰۲۳: پایگاه مشتریان به بیش از ۲۵۰ مشتری سازمانی رسید. متوسط اندازه معاملات ۷۵ درصد افزایش یافت و به ۱۲۵،۰۰۰ دلار رسید. استفاده از پلتفرم ۳۰۰ درصد نسبت به سال قبل افزایش یافت. بخش‌های کلیدی: مالی، سلامت و فناوری.",
            "metadata": {
                "source": "معیارهای_رشد",
                "date": "2023-12",
                "type": "رشد",
                "language": "fa"
            }
        },
        {
            "text": "فناوری‌های ماکس: ساخته شده بر پایه مدل‌های زبانی پیشرفته با پیاده‌سازی اختصاصی RAG. زیرساخت شامل خوشه‌های GPU افزونه در ۳ منطقه. تضمین دسترس‌پذیری ۹۹.۹۹ درصد برای مشتریان سازمانی.",
            "metadata": {
                "source": "مستندات_فنی",
                "date": "2024-01",
                "type": "فناوری",
                "language": "fa"
            }
        }
    ]
    
    for doc in docs:
        response = requests.post(f"{BASE_URL}/vector_db/add_document", json=doc)
        print(f"Document added (type: {doc['metadata']['type']}):", response.json())

def clear_collection():
    """Clear all documents from the collection"""
    response = requests.post(f"{BASE_URL}/vector_db/clear_collection")
    print("Collection cleared:", response.json())

if __name__ == "__main__":
    # Clear existing collection (optional)
    clear_collection()
    
    # Initialize and add documents
    initialize_collection()
    add_documents()