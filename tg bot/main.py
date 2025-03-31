import telebot

from telebot import types

token = '2092994879:AAH0ceNOzO4-S8d6bCykpvxlz0kli-lw_OI'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start", "menu"])
def start_info(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_my_site = types.KeyboardButton("Вырезать аудио из видео")
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Привет пользователь, я твой помощник, с чем тебе помочь ", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def audio(message):
    if message.text == "Вырезать аудио из видео":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_my_site = types.KeyboardButton("Ссылка")
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, "Нажмите кнопку отправить ссылку", reply_markup=markup)

    elif message.text == "Ссылка":
        bot.send_message(message.chat.id, "SUKA BLYAD")
        from pytube import YouTube
        url = YouTube(message.text)
        bot.send_message(message.chat.id, "Загрузка")
        video = url.streams.get_audio_only()
        bot.send_audio(message.chat.id, video)

    else:
        bot.send_message(message.chat.id, "PYTHON BLYAD ")





bot.polling(True)
