# utils/parsers.py

import requests
from datetime import datetime
from db.queries import add_rate

# --- Константи з URL-адресами для різних джерел ---
NBU_API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
PRIVAT_API_URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
MONO_API_URL = "https://api.monobank.ua/bank/currency"
MINFIN_URL = "https://minfin.com.ua/ua/currency/usd/"

REQUEST_TIMEOUT = 5  # Таймаут для HTTP-запитів у секундах

# --- Парсер курсу USD з НБУ ---


def get_usd_nbu():
    """
    Отримати курс USD з НБУ API та зберегти в БД.
    """
    try:
        response = requests.get(NBU_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        for item in data:
            if item["cc"] == "USD":
                rate = item["rate"]
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "USD", "NBU", rate)  # Зберігаємо в БД
                return rate, date
    except Exception as e:
        print(f"Помилка при запиті до NBU (USD): {e}")
    return None, None

# --- Парсер курсу USD з ПриватБанку ---


def get_usd_privat():
    """
    Отримати курс USD з ПриватБанку API та зберегти в БД.
    """
    try:
        response = requests.get(PRIVAT_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        for item in data:
            if item["ccy"] == "USD" and item["base_ccy"] == "UAH":
                rate = float(item["sale"])
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "USD", "PrivatBank", rate)
                return rate, date
    except Exception as e:
        print(f"Помилка при запиті до ПриватБанку (USD): {e}")
    return None, None

# --- Парсер курсу USD з Monobank ---


def get_usd_mono():
    """
    Отримати курс USD з Monobank API та зберегти в БД.
    """
    try:
        response = requests.get(MONO_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        # USD: currencyCodeA=840, currencyCodeB=980 (UAH)
        for item in data:
            if item.get("currencyCodeA") == 840 and item.get("currencyCodeB") == 980:
                rate = item.get("rateSell") or item.get("rateCross")
                if rate:
                    date = datetime.now().strftime("%Y-%m-%d")
                    add_rate(date, "USD", "Monobank", rate)
                    return rate, date
    except Exception as e:
        print(f"Помилка при запиті до Monobank (USD): {e}")
    return None, None

# --- Парсер курсу USD з Мінфін (HTML-парсинг) ---


def get_usd_minfin():
    """
    Отримати курс USD з сайту Мінфін (HTML-парсинг) та зберегти в БД.
    """
    try:
        from bs4 import BeautifulSoup
        response = requests.get(MINFIN_URL, headers={
                                "User-Agent": "Mozilla/5.0"}, timeout=REQUEST_TIMEOUT)
        soup = BeautifulSoup(response.text, "html.parser")
        # Знаходимо перший курс продажу USD (може змінюватись верстка!)
        rate_tag = soup.find("div", class_="sc-1x32wa2-9")
        if rate_tag:
            try:
                rate = float(rate_tag.text.replace(",", "."))
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "USD", "Minfin", rate)
                return rate, date
            except Exception as e:
                print(f"Помилка при парсингу курсу з Мінфін: {e}")
    except Exception as e:
        print(f"Помилка при запиті до Мінфін (USD): {e}")
    return None, None

# --- Парсер курсу EUR з НБУ ---


def get_eur_nbu():
    """
    Отримати курс EUR з НБУ API та зберегти в БД.
    """
    try:
        response = requests.get(NBU_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        for item in data:
            if item["cc"] == "EUR":
                rate = item["rate"]
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "EUR", "NBU", rate)
                return rate, date
    except Exception as e:
        print(f"Помилка при запиті до NBU (EUR): {e}")
    return None, None

# --- Парсер курсу GBP з НБУ ---


def get_gbp_nbu():
    """
    Отримати курс GBP з НБУ API та зберегти в БД.
    """
    try:
        response = requests.get(NBU_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        for item in data:
            if item["cc"] == "GBP":
                rate = item["rate"]
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "GBP", "NBU", rate)
                return rate, date
    except Exception as e:
        print(f"Помилка при запиті до NBU (GBP): {e}")
    return None, None

# --- Парсер курсу PLN з НБУ ---


def get_pln_nbu():
    """
    Отримати курс PLN з НБУ API та зберегти в БД.
    """
    try:
        response = requests.get(NBU_API_URL, timeout=REQUEST_TIMEOUT)
        data = response.json()
        for item in data:
            if item["cc"] == "PLN":
                rate = item["rate"]
                date = datetime.now().strftime("%Y-%m-%d")
                add_rate(date, "PLN", "NBU", rate)
                return rate, date
    except Exception as e:
        print(f"Помилка при запиті до NBU (PLN): {e}")
    return None, None

# --- Тут можна додати парсери для інших валют і джерел ---
# Можна додати парсинг з інших джерел (наприклад, Мінфін) через BeautifulSoup