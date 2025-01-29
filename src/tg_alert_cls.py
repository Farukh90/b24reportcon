import datetime
import time

import requests

from constants import B24REPORT_BOT, B24REPORT_CHAT_ID, B24REPORT_THREADS


class TelegramAlert:
    def __init__(self, token, chat_id, threads=None):
        """
        Инициализация Telegram Bot
        :param token: Токен Telegram бота
        :param chat_id: ID группы или чата
        :param threads: Словарь с названиями тем и их ID
        """
        self.token = token
        self.chat_id = chat_id
        self.threads = threads or {}  # Словарь с темами
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message, thread_name=None):
        """
        Отправляет сообщение в телеграм
        :param message: Текст сообщения
        :param thread_name: Название темы (опционально)
        """
        thread_id = self.threads.get(thread_name) if thread_name else None
        params = {
            "text": message,
            "chat_id": self.chat_id,
            "message_thread_id": thread_id,
            "parse_mode": "HTML",
        }

        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            print(f"Сообщение отправлено в тему '{thread_name or 'общую'}': {message}")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")

        time.sleep(1)  # Задержка между запросами

    def send_pdf(self, file_path, thread_name=None, caption=None):
        """
        Отправляет PDF-файл в телеграм
        :param file_path: Путь к PDF-файлу
        :param thread_name: Название темы (опционально)
        :param caption: Подпись к файлу (опционально)
        """
        thread_id = self.threads.get(thread_name) if thread_name else None
        params = {
            "chat_id": self.chat_id,
            "caption": caption,
            "message_thread_id": thread_id,
        }
        with open(file_path, "rb") as file:
            files = {"document": file}

            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendDocument",
                params=params,
                files=files,
            )
        if response.status_code == 200:
            print(f"Файл '{file_path}' отправлен в тему '{thread_name or 'общую'}'")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")
            time.sleep(1)  # Задержка между запросами

    def send_file(
        self, file_path, file_type="document", thread_name=None, caption=None
    ):
        """
        Отправляет файл в телеграм
        :param file_path: Путь к файлу
        :param file_type: Тип файла ("document", "photo", "video", "audio")
        :param thread_name: Название темы (опционально)
        :param caption: Подпись к файлу (опционально)
        """
        # Сопоставление типов файлов с методами API
        file_methods = {
            "document": "sendDocument",
            "photo": "sendPhoto",
            "video": "sendVideo",
            "audio": "sendAudio",
        }

        if file_type not in file_methods:
            raise ValueError(
                f"Неподдерживаемый тип файла: {file_type}. Поддерживаются: {', '.join(file_methods.keys())}"
            )

        thread_id = self.threads.get(thread_name) if thread_name else None

        params = {
            "chat_id": self.chat_id,
            "caption": caption,
        }
        if thread_id:
            params["message_thread_id"] = thread_id

        # Открытие файла и отправка
        with open(file_path, "rb") as file:
            files = {file_type: file}
            time.sleep(1)  # Задержка между запросами
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/{file_methods[file_type]}",
                params=params,
                files=files,
            )
        if response.status_code == 200:
            print(f"Файл '{file_path}' отправлен в тему '{thread_name or 'общую'}'")
        else:
            print(f"Ошибка: {response.status_code} - {response.text}")


# Пример использования
if __name__ == "__main__":
    bot = TelegramAlert(B24REPORT_BOT, B24REPORT_CHAT_ID, B24REPORT_THREADS)
    # bot.send_message("Привет, это сообщение для всех!")  # Отправка в общую тему
    bot.send_message("rwwrwrg", thread_name="Раскрои ФРС")  # В тему "обсуждение"
    # bot.send_message("Сообщение об ошибке", thread_name="ошибки")  # В тему "ошибки"
    # bot.send_pdf(r"C:\1\автоматизация.pdf", thread_name="Раскрои ФРС", caption="Это мой PDF-файл")  # Отправка PDF
    # bot.send_file(r"C:\1\woodw.jpg", file_type="photo", caption="Это пример фото")
