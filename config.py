# config.py

import os
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен Telegram-бота
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # ID адміністратора

# Назва файлу бази даних
DB_PATH = "db/currency.db"  # Шлях до бази даних SQLite
