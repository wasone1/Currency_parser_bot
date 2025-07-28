# main.py

import asyncio
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db.queries import init_db
from handlers import user
from aiogram.types import BotCommand

async def main():
    # 1. Ініціалізуємо базу даних
    init_db()

    # 2. Перевіряємо наявність токена
    if not BOT_TOKEN:
        print("❌ Помилка: BOT_TOKEN не знайдено! Додайте токен у .env файл.")
        sys.exit(1)

    # 3. Створюємо бота та диспетчер
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Додаємо меню команд
    commands = [
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="admin", description="Адмін-панель (тільки для адміністратора)"),
        BotCommand(command="usd", description="Курс долара (НБУ)"),
        BotCommand(command="eur", description="Курс євро (НБУ)"),
        BotCommand(command="compare", description="Порівняння курсу USD з різних джерел"),
        BotCommand(command="currency", description="Вибір валюти та порівняння курсів"),
        BotCommand(command="history", description="Історія курсу USD"),
        BotCommand(command="chart", description="Графік курсу USD"),
        BotCommand(command="subscribe", description="Підписка на розсилку"),
        BotCommand(command="unsubscribe", description="Відписка від розсилки"),
        BotCommand(command="help", description="Допомога"),
    ]
    await bot.set_my_commands(commands)

    # 4. Підключаємо роутери
    dp.include_router(user.router)

    # 5. Запускаємо бота
    print("Бот запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинено.")