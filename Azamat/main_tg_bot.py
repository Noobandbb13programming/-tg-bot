import asyncio
import logging
import os
import gspread
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from oauth2client.service_account import ServiceAccountCredentials

# Загружаем переменные из .env
load_dotenv()

# Получаем токен бота и ID таблицы из .env
TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDENTIALS_FILE = "credentials.json"

# Авторизация в Google Sheets
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # Первый лист
    logger.info("Успешное подключение к Google Sheets")
except Exception as e:
    logger.error(f"Ошибка подключения к Google Sheets: {e}")
    sheet = None  # Если ошибка, оставляем sheet пустым

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Отправь мне ID заказа, и я найду его в базе.")


@dp.message()
async def find_order(message: Message):
    if not sheet:
        await message.answer("⚠️ Ошибка: Бот не подключен к Google Sheets.")
        return

    order_id = message.text.strip()

    try:
        data = sheet.get_all_values()
        headers = data[0]
        rows = data[1:]

        found_orders = [row for row in rows if row[1] == order_id]

        if found_orders:
            response = ""
            for order in found_orders:
                response += (
                    f"📅 Дата: {order[0]}\n"
                    f"🆔 ID заказа: {order[1]}\n"
                    f"📜 Описание: {order[2]}\n"
                    f"📦 Товары: {order[3]}\n"
                    f"🔢 Количество: {order[4]}\n"
                    f"⚖️ Вес: {order[5]}\n"
                    f"🚛 ID груза: {order[6]}\n\n"
                )
        else:
            response = "❌ Заказ не найден. Проверьте ID."

    except Exception as e:
        response = f"⚠️ Ошибка при поиске: {e}"
        logger.error(f"Ошибка при поиске заказа: {e}")

    await message.answer(response)


async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
