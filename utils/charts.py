# utils/charts.py

import matplotlib.pyplot as plt
import os
import time


def create_chart(history, currency="USD", user_id=None):
    """
    Створює графік курсу за історією.
    history — список кортежів (date, rate)
    currency — код валюти (для підпису і імені файлу)
    user_id — (опціонально) додається до імені файлу для унікальності
    """
    # Розпаковуємо дати і курси
    dates = [date for date, rate in history]
    rates = [rate for date, rate in history]

    # Створюємо фігуру і будуємо графік
    plt.figure(figsize=(8, 4))
    plt.plot(dates, rates, marker='o')
    plt.title(f"Курс {currency} за останні {len(history)} днів")
    plt.xlabel("Дата")
    plt.ylabel("Курс, грн")
    plt.grid(True)
    plt.tight_layout()

    # Генеруємо унікальне ім'я файлу (user_id + timestamp)
    timestamp = int(time.time())
    if user_id:
        file_path = f"chart_{currency}_{user_id}_{timestamp}.png"
    else:
        file_path = f"chart_{currency}_{timestamp}.png"

    # Зберігаємо графік у файл з обробкою помилок
    try:
        plt.savefig(file_path)
    except Exception as e:
        print(f"Помилка при збереженні графіка: {e}")
        plt.close()
        return None
    plt.close()

    return file_path


def cleanup_old_charts(directory=".", prefix="chart_", max_age_sec=3600):
    """
    Видаляє старі графіки, щоб не захаращувати диск.
    directory — де шукати файли
    prefix — початок імені файлу
    max_age_sec — максимальний вік файлу у секундах (за замовчуванням 1 година)
    """
    now = time.time()
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith(".png"):
            file_path = os.path.join(directory, filename)
            try:
                if now - os.path.getmtime(file_path) > max_age_sec:
                    os.remove(file_path)
                    print(f"Видалено старий графік: {filename}")
            except Exception as e:
                print(f"Помилка при видаленні {filename}: {e}")