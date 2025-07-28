# handlers/user.py

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InputFile, FSInputFile
from db.queries import (
    add_subscriber, remove_subscriber, get_history, get_latest_rate, increment_command_stat, get_subscribers, get_all_stats
)
from utils.parsers import get_usd_nbu, get_eur_nbu, get_usd_privat, get_usd_mono, get_usd_minfin, get_gbp_nbu, get_pln_nbu
from utils.charts import create_chart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_ID

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    increment_command_stat("start")
    if message.from_user:
        add_subscriber(message.from_user.id)
    await message.answer(
        "Вітаю! Я бот для відстеження курсу валют 💸\n"
        "Доступні команди:\n"
        "/admin — адмін-панель (тільки для адміністратора)\n"
        "/usd — курс долара\n"
        "/eur — курс євро\n"
        "/compare — порівняння курсів\n"
        "/currency — вибір валюти та порівняння курсів\n"
        "/history — історія курсів\n"
        "/chart — графік\n"
        "/subscribe — підписка на розсилку\n"
        "/unsubscribe — відписка"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    increment_command_stat("help")
    await message.answer(
        "Доступні команди:\n"
        "/admin — адмін-панель (тільки для адміністратора)\n"
        "/usd — курс долара\n"
        "/eur — курс євро\n"
        "/compare — порівняння курсів\n"
        "/currency — вибір валюти та порівняння курсів\n"
        "/history — історія курсів\n"
        "/chart — графік\n"
        "/subscribe — підписка на розсилку\n"
        "/unsubscribe — відписка"
    )

@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if not message.from_user or message.from_user.id != ADMIN_ID:
        await message.answer("⛔️ Доступ заборонено.")
        return

    subs = get_subscribers()
    stats = get_all_stats()
    text = f"👑 Адмін-панель\n\n"
    text += f"Підписників: {len(subs)}\n\n"
    text += "Статистика команд:\n"
    for cmd, count in stats:
        text += f"/{cmd}: {count}\n"
    await message.answer(text)

@router.message(Command("usd"))
async def cmd_usd(message: types.Message):
    increment_command_stat("usd")
    rate, date = get_usd_nbu()  # Парсимо курс і одразу зберігаємо в БД
    if rate:
        await message.answer(f"Курс USD (НБУ): {rate} грн\nДата: {date}")
    else:
        await message.answer("Не вдалося отримати курс USD.")

@router.message(Command("eur"))
async def cmd_eur(message: types.Message):
    increment_command_stat("eur")
    rate, date = get_eur_nbu()
    if rate:
        await message.answer(f"Курс EUR (НБУ): {rate} грн\nДата: {date}")
    else:
        await message.answer("Не вдалося отримати курс EUR.")

@router.message(Command("compare"))
async def cmd_compare(message: types.Message):
    increment_command_stat("compare")
    nbu, _ = get_usd_nbu()
    privat, _ = get_usd_privat()
    mono, _ = get_usd_mono()
    minfin, _ = get_usd_minfin()

    text = "Порівняння курсу USD:\n"
    text += f"НБУ: {nbu if nbu else 'н/д'} грн\n"
    text += f"ПриватБанк: {privat if privat else 'н/д'} грн\n"
    text += f"Монобанк: {mono if mono else 'н/д'} грн\n"
    text += f"Мінфін: {minfin if minfin else 'н/д'} грн\n"

    await message.answer(text)

@router.message(Command("currency"))
async def cmd_currency(message: types.Message):
    increment_command_stat("currency")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="USD"), KeyboardButton(text="EUR")],
            [KeyboardButton(text="PLN"), KeyboardButton(text="BTC")],
            [KeyboardButton(text="GBP")],
		  ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("Оберіть валюту:", reply_markup=keyboard)

@router.message(Command("history"))
async def cmd_history(message: types.Message):
    increment_command_stat("history")
    history = get_history("USD", "NBU", days=7)
    if history:
        text = "Історія курсу USD (НБУ):\n"
        text += "\n".join([f"{date}: {rate} грн" for date, rate in history])
        await message.answer(text)
    else:
        await message.answer("Історія порожня.")

@router.message(Command("subscribe"))
async def cmd_subscribe(message: types.Message):
    increment_command_stat("subscribe")
    if message.from_user:
        add_subscriber(message.from_user.id)
    await message.answer("Ви підписані на щоденну розсилку курсу!")

@router.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: types.Message):
    increment_command_stat("unsubscribe")
    if message.from_user:
        remove_subscriber(message.from_user.id)
    await message.answer("Ви відписалися від розсилки.")

@router.message(Command("chart"))
async def cmd_chart(message: types.Message):
    increment_command_stat("chart")
    history = get_history("USD", "NBU", days=7)
    if not history:
        await message.answer("Історія порожня.")
        return
    file_path = create_chart(history)
    input_file = FSInputFile(file_path)
    await message.answer_photo(input_file, caption="Графік курсу USD (НБУ) за 7 днів")

@router.message()
async def handle_currency_choice(message: types.Message):
    currency = message.text.upper()
    if currency not in ["USD", "EUR", "PLN", "BTC", "GBP"]:
        return  # Ігноруємо інші повідомлення

    # Парсимо курс з різних джерел (приклад для USD/EUR)
    if currency == "USD":
        nbu, _ = get_usd_nbu()
        privat, _ = get_usd_privat()
        mono, _ = get_usd_mono()
        minfin, _ = get_usd_minfin()
        text = "Порівняння курсу USD:\n"
        text += f"НБУ: {nbu if nbu else 'н/д'} грн\n"
        text += f"ПриватБанк: {privat if privat else 'н/д'} грн\n"
        text += f"Монобанк: {mono if mono else 'н/д'} грн\n"
        text += f"Мінфін: {minfin if minfin else 'н/д'} грн\n"
    elif currency == "EUR":
        # Додай аналогічні парсери для EUR (get_eur_nbu, get_eur_privat, ...)
        text = "Порівняння курсу EUR:\n(реалізуй парсери для EUR)"
    elif currency == "PLN":
        nbu, _ = get_pln_nbu()
        text = f"Курс PLN (НБУ): {nbu if nbu else 'н/д'} грн\n"
    elif currency == "BTC":
        text = "Порівняння курсу BTC:\n(реалізуй парсери для BTC)"
    elif currency == "GBP":
        nbu, _ = get_gbp_nbu()
        text = f"Курс GBP (НБУ): {nbu if nbu else 'н/д'} грн\n"
    else:
        text = "Невідома валюта."

    await message.answer(text)