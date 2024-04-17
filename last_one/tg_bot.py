import sys
import json
import telebot
import datetime
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Если не будет работать путь, то используй строчку ниже
# config_path = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])+'\\config.json'

with open(r'last_one\config.json') as file:
    data = json.load(file)

TOKEN = data['tg_token']

bot = telebot.TeleBot(TOKEN)

sessions = {}

def log_out(string):
    print('[LOG OUTPUT] : '+string)
    sys.stdout.flush()

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Бот работает норально(пока что)')
    elif message.text == '/test':
        print('[LOG OUTPUT] : Вы что-то тестируйте!')
        sys.stdout.flush()

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    log_out('call = true')


log_out('Bot is ready.')
bot.infinity_polling()