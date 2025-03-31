from string import punctuation

from aiogram import F, types, Router

from tg_bot_aiorgramm.filters.chat_types import ChatTypeFilters


user_group_router = Router()
user_group_router.message.filter(ChatTypeFilters(['group', 'supergroup']))


restricted_word = {'кабан', 'хомяк', 'выхухоль'}


def clean_text(text: str):
    return text.translate(str.maketrans("","", punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_word.intersection(clean_text(message.text.lower()).split()):
        await message.answer(f"{message.from_user.first_name}, соблюддайте порядок в чате")
        await message.delete()
