import telebot
from telebot import types
import random
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


bot = telebot.TeleBot(os.getenv('TG_TOKEN'))

numbers = {}


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_start = types.InlineKeyboardButton(text='Сыграть', callback_data='start')
        # И добавляем кнопку на экран
        keyboard.add(key_start)
        bot.send_message(message.from_user.id, text='Давай сыграем в игру "Больше - меньше"', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    else:
        if is_int(message.text):
            if message.from_user.id in numbers:
                if int(message.text) < 1 or int(message.text) > 100:
                    bot.send_message(message.from_user.id, "Введите целое число от 1 до 100")
                elif int(message.text) > numbers[message.from_user.id]:
                    bot.send_message(message.from_user.id, "Меньше")
                elif int(message.text) < numbers[message.from_user.id]:
                    bot.send_message(message.from_user.id, "Больше")
                else:
                    keyboard = types.InlineKeyboardMarkup()
                    key_start = types.InlineKeyboardButton(text='Сыграть', callback_data='start')
                    keyboard.add(key_start)
                    bot.send_message(message.from_user.id, text='Правильно, ты выиграл! Давай сыграем ещё раз', reply_markup=keyboard)
            else:
                # Готовим кнопки
                keyboard = types.InlineKeyboardMarkup()
                # По очереди готовим текст и обработчик для каждого знака зодиака
                key_start = types.InlineKeyboardButton(text='Сыграть', callback_data='start')
                # И добавляем кнопку на экран
                keyboard.add(key_start)
                bot.send_message(message.from_user.id, text='Давай сыграем в игру "Больше - меньше"', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, "Введите целое число от 1 до 100")


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "start":
        bot.send_message(call.message.chat.id, "Я загадал число от 1 до 100, попробуй его угадать.")
        global numbers
        numbers[call.message.chat.id] = random.randint(1, 100)


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


bot.polling(none_stop=True, interval=0)