from dotenv import load_dotenv
load_dotenv()

import telebot
import pandas as pd
import json
import os

import helpers

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

COMMANDS = {
    'current': 'current'
}
bot.set_my_commands([telebot.types.BotCommand(k, v) for k, v in COMMANDS.items()])



@bot.message_handler(commands=['current'])
def current(message):
    current = helpers.find_state(-1)
    text = helpers.format_state(current)
    return bot.reply_to(message, text)
    

bot.infinity_polling()