from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from tg_bot_aiorgramm.filters.chat_types import ChatTypeFilters

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilters(['private']))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hello, I am Helper BOT")


@user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command('menu'), F.text.lower() == "меню"))
async def menu_cmd(message: types.Message):
    await message.answer("Вот меню:")


@user_private_router.message(F.text.lower() == "О нас")
@user_private_router.message(Command('about'))
async def menu_cmd(message: types.Message):
    await message.answer("О нас:")


@user_private_router.message((F.text.lower().contains("оплат")) | (F.text.lower() == "Варианты оплаты"))
@user_private_router.message(Command('payment'))
async def menu_cmd(message: types.Message):
    await message.answer("Варианты оплаты:")


@user_private_router.message((F.text.lower().contains("доставк")) | (F.text.lower() == "Варианты доставки"))
@user_private_router.message(Command('shipping'))
async def menu_cmd(message: types.Message):
    await message.answer("Варианты доставки:")



