import asyncio
import logging
import os
import json
from aiohttp import web
import gspread
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from oauth2client.service_account import ServiceAccountCredentials

# Загружаем переменные окружения
load_dotenv()

# Получаем переменные
TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
CREDENTIALS_JSON = os.getenv("CREDENTIALS_FILE")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к Google Sheets через содержимое переменной CREDENTIALS_JSON
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    if not CREDENTIALS_JSON:
        raise Exception("Переменная окружения CREDENTIALS_JSON не установлена")
    credentials_dict = json.loads(CREDENTIALS_JSON)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # Открываем первый лист
    logger.info("✅ Подключение к Google Sheets успешно")
except Exception as e:
    logger.error(f"❌ Ошибка подключения к Google Sheets: {e}")
    sheet = None

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Отправь мне ID заказа, и я найду его в базе.")

# Обработчик поиска заказа
@dp.message()
async def find_order(message: types.Message):
    if not sheet:
        await message.answer("⚠️ Ошибка подключения к Google Sheets.")
        return

    order_id = message.text.strip()
    try:
        data = sheet.get_all_values()
        headers = data[0]
        rows = data[1:]
        found_orders = [row for row in rows if row[1] == order_id]

        if found_orders:
            response = "\n\n".join(
                f"📅 Дата: {order[0]}\n🆔 ID заказа: {order[1]}\n📜 Описание: {order[2]}\n"
                f"📦 Товары: {order[3]}\n🔢 Количество: {order[4]}\n⚖️ Вес: {order[5]}\n🚛 ID груза: {order[6]}"
                for order in found_orders
            )
        else:
            response = "❌ Заказ не найден. Проверьте ID."
    except Exception as e:
        response = f"⚠️ Ошибка: {e}"
        logger.error(f"Ошибка при поиске заказа: {e}")

    await message.answer(response)

# Обработчик для вебхука
async def webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Установка вебхука при запуске
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logger.info("🚀 Вебхук установлен!")

# Основная функция для запуска веб-сервера
async def main():
    app = web.Application()
    app.router.add_post("/", webhook)
    await on_startup()
    return app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Railway передает порт через переменную окружения PORT
    web.run_app(main(), port=port)
