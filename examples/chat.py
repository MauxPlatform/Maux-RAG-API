from openai import OpenAI
import json
from typing import List, Dict, Optional
import sys
import locale
import os

# Configure console encoding for Windows
if sys.platform == "win32":
    os.system("chcp 65001")  # Set UTF-8 encoding
    sys.stdout.reconfigure(encoding='utf-8')

# تنظیمات اولیه کلاینت
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy-key"  # کلید API در این نمونه استفاده نمی‌شود
)

def print_persian(text: str, end: str = "\n", flush: bool = True) -> None:
    """
    Print Persian text with proper encoding handling
    """
    try:
        print(text, end=end, flush=flush)
    except UnicodeEncodeError:
        # Fallback for environments where UTF-8 printing fails
        encoded_text = text.encode('utf-8', errors='replace').decode('utf-8')
        print(encoded_text, end=end, flush=flush)

def chat_completion_simple(
    messages: List[Dict[str, str]], 
    model: str = "gpt-4o-mini"
) -> Optional[str]:
    """
    ارسال یک درخواست چت ساده و دریافت پاسخ
    
    Args:
        messages: لیست پیام‌ها در قالب استاندارد OpenAI
        model: نام مدل مورد استفاده
    
    Returns:
        متن پاسخ یا None در صورت خطا
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print_persian(f"خطا در درخواست: {str(e)}")
        return None

def chat_completion_stream(
    messages: List[Dict[str, str]], 
    model: str = "gpt-4o-mini"
) -> None:
    """
    ارسال یک درخواست چت با حالت stream و نمایش پاسخ‌ها به صورت زنده
    
    Args:
        messages: لیست پیام‌ها در قالب استاندارد OpenAI
        model: نام مدل مورد استفاده
    """
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        
        print_persian("پاسخ: ", end="")
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print_persian(chunk.choices[0].delta.content, end="")
        print_persian("\n")
    except Exception as e:
        print_persian(f"خطا در درخواست stream: {str(e)}")

def test_simple_completion():
    """تست درخواست چت ساده"""
    messages = [
        {
            "role": "system",
            "content": "شما یک دستیار مطلع با دسترسی به اطلاعات شرکت ماکس هستید."
        },
        {
            "role": "user",
            "content": "درآمد شرکت ماکس در سه‌ماهه چهارم ۲۰۲۳ چقدر بود؟"
        }
    ]
    
    print_persian("\n=== تست درخواست ساده ===")
    response = chat_completion_simple(messages)
    if response:
        print_persian(f"پاسخ: {response}\n")

def test_streaming_completion():
    """تست درخواست چت با حالت stream"""
    messages = [
        {
            "role": "system",
            "content": "شما یک دستیار مطلع با دسترسی به اطلاعات شرکت ماکس هستید."
        },
        {
            "role": "user",
            "content": "لطفاً در مورد محصولات و قیمت‌گذاری شرکت ماکس توضیح دهید."
        }
    ]
    
    print_persian("\n=== تست درخواست stream ===")
    chat_completion_stream(messages)

def test_multi_turn_conversation():
    """تست مکالمه چند مرحله‌ای"""
    conversation = [
        {
            "role": "system",
            "content": "شما یک دستیار مطلع با دسترسی به اطلاعات شرکت ماکس هستید."
        },
        {
            "role": "user",
            "content": "شرکت ماکس چند کارمند دارد؟"
        }
    ]
    
    print_persian("\n=== تست مکالمه چند مرحله‌ای ===")
    
    # مرحله اول
    response = chat_completion_simple(conversation)
    if response:
        print_persian(f"پاسخ ۱: {response}\n")
        conversation.extend([
            {"role": "assistant", "content": response},
            {"role": "user", "content": "این کارمندان در کدام دفاتر مستقر هستند؟"}
        ])
    
    # مرحله دوم
    response = chat_completion_simple(conversation)
    if response:
        print_persian(f"پاسخ ۲: {response}\n")

def run_all_tests():
    """اجرای تمام تست‌ها"""
    test_simple_completion()
    test_streaming_completion()
    test_multi_turn_conversation()

if __name__ == "__main__":
    run_all_tests()