# Currency Rate Telegram Bot

Телеграм-бот для отримання актуального курсу валют (USD, EUR, PLN, GBP) з різних джерел (НБУ, ПриватБанк, Monobank, Мінфін), зберігання історії в SQLite, підписки на розсилку та побудови графіків.

## Функціонал

- Отримання курсу валют з різних джерел (/usd, /eur, /compare, /currency)
- Порівняння курсів між банками
- Історія курсів (/history)
- Графік зміни курсу (/chart)
- Підписка на розсилку (/subscribe, /unsubscribe)
- Адмін-панель зі статистикою (/admin)
- Зберігання історії у SQLite

## Технології

- Python 3.10+
- aiogram
- requests
- beautifulsoup4
- matplotlib
- SQLite
- python-dotenv

## Запуск

1. Клонувати репозиторій:
    ```
    git clone https://github.com/yourusername/currency-bot.git
    cd currency-bot
    ```
2. Встановити залежності:
    ```
    pip install -r requirements.txt
    ```
3. Створити файл `.env` на основі `.env.example` і додати свій Telegram Bot Token:
    ```
    BOT_TOKEN=тут_твій_токен
    ADMIN_ID=тут_твій_telegram_id
    ```
4. Запустити бота:
    ```
    python main.py
    ```

## Приклад команд

- `/start` — запуск бота
- `/usd` — курс долара (НБУ)
- `/eur` — курс євро (НБУ)
- `/compare` — порівняння курсів USD з різних джерел
- `/currency` — вибір валюти та порівняння курсів
- `/history` — історія курсу USD
- `/chart` — графік курсу USD
- `/subscribe` — підписка на розсилку
- `/unsubscribe` — відписка від розсилки
- `/admin` — адмін-панель (тільки для адміністратора)
- `/help` — список команд

## Деплой через Docker (опціонально)

1. Встановити Docker.
2. Запустити:
    ```
    docker-compose up --build
    ```

## Ліцензія

MIT License

---

**Автор:** Mykyta Voroniuk