import os

from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()


B24REPORT_BOT = os.getenv("B24REPORT_BOT")
B24REPORT_CHAT_ID = os.getenv("B24REPORT_CHAT_ID")
B24REPORT_THREADS = {
    "общая": None,
    "отчеты по выполненным работам b24": 2,
}
