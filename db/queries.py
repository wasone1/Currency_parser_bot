# db/queries.py

import sqlite3
from datetime import datetime
from config import DB_PATH

# --- SQL-запити як константи ---
SQL_CREATE_RATES = """
    CREATE TABLE IF NOT EXISTS rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        currency TEXT NOT NULL,
        source TEXT NOT NULL,
        rate REAL NOT NULL
    )
"""
SQL_CREATE_SUBSCRIBERS = """
    CREATE TABLE IF NOT EXISTS subscribers (
        user_id INTEGER PRIMARY KEY,
        subscribed INTEGER DEFAULT 1
    )
"""
SQL_CREATE_STATS = """
    CREATE TABLE IF NOT EXISTS stats (
        command TEXT PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
"""
SQL_INSERT_RATE = """
    INSERT INTO rates (date, currency, source, rate)
    VALUES (?, ?, ?, ?)
"""
SQL_SELECT_LATEST_RATE = """
    SELECT rate, date FROM rates
    WHERE currency = ? AND source = ?
    ORDER BY date DESC
    LIMIT 1
"""
SQL_SELECT_HISTORY = """
    SELECT date, rate FROM rates
    WHERE currency = ? AND source = ?
    ORDER BY date DESC
    LIMIT ?
"""
SQL_INSERT_SUBSCRIBER = """
    INSERT OR IGNORE INTO subscribers (user_id, subscribed)
    VALUES (?, 1)
"""
SQL_UPDATE_UNSUBSCRIBE = """
    UPDATE subscribers SET subscribed = 0 WHERE user_id = ?
"""
SQL_SELECT_SUBSCRIBERS = """
    SELECT user_id FROM subscribers WHERE subscribed = 1
"""
SQL_INCREMENT_COMMAND_STAT = """
    INSERT INTO stats (command, count) VALUES (?, 1)
    ON CONFLICT(command) DO UPDATE SET count = count + 1
"""
SQL_SELECT_ALL_STATS = """
    SELECT command, count FROM stats
"""


def get_connection():
    # Створює нове з'єднання з SQLite-базою для кожного запиту
    return sqlite3.connect(DB_PATH)


def init_db():
    """Створює всі необхідні таблиці, якщо їх ще немає."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_CREATE_RATES)
            cursor.execute(SQL_CREATE_SUBSCRIBERS)
            cursor.execute(SQL_CREATE_STATS)
            conn.commit()
    except Exception as e:
        print(f"Помилка ініціалізації БД: {e}")


def add_rate(date, currency, source, rate):
    """Додає новий курс у таблицю rates."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_RATE, (date, currency, source, rate))
            conn.commit()
    except Exception as e:
        print(f"Помилка при додаванні курсу: {e}")


def get_latest_rate(currency, source):
    """Повертає останній курс для заданої валюти і джерела."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_SELECT_LATEST_RATE, (currency, source))
            return cursor.fetchone()
    except Exception as e:
        print(f"Помилка при отриманні останнього курсу: {e}")
        return None


def get_history(currency, source, days=7):
    """Повертає історію курсів за N днів (від найстарішого до найновішого)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_SELECT_HISTORY, (currency, source, days))
            return cursor.fetchall()[::-1]  # Від найстарішого до найновішого
    except Exception as e:
        print(f"Помилка при отриманні історії курсів: {e}")
        return []


def add_subscriber(user_id):
    """Додає нового підписника (або ігнорує, якщо вже є)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_INSERT_SUBSCRIBER, (user_id,))
            conn.commit()
    except Exception as e:
        print(f"Помилка при додаванні підписника: {e}")


def remove_subscriber(user_id):
    """Відмічає підписника як відписаного (subscribed = 0)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_UPDATE_UNSUBSCRIBE, (user_id,))
            conn.commit()
    except Exception as e:
        print(f"Помилка при відписці: {e}")


def get_subscribers():
    """Повертає список user_id всіх підписаних користувачів."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_SELECT_SUBSCRIBERS)
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Помилка при отриманні підписників: {e}")
        return []


def increment_command_stat(command):
    """Збільшує лічильник викликів команди (або створює запис, якщо його ще немає)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_INCREMENT_COMMAND_STAT, (command,))
            conn.commit()
    except Exception as e:
        print(f"Помилка при оновленні статистики команди: {e}")


def get_all_stats():
    """Повертає статистику по всіх командах (список кортежів (command, count))."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SQL_SELECT_ALL_STATS)
            return cursor.fetchall()
    except Exception as e:
        print(f"Помилка при отриманні статистики: {e}")
        return []
