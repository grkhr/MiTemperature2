from dotenv import load_dotenv
load_dotenv()

import telebot
import pandas as pd
import json
import pprint
import os

import helpers

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

COMMANDS = {
    'current': 'current',
    'get_config': 'get_config',
    'change_config': 'change config'
}
bot.set_my_commands([telebot.types.BotCommand(k, v) for k, v in COMMANDS.items()])

def init_markup(buttons, row_width=1):
    markup = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [telebot.types.InlineKeyboardButton(v, callback_data=k) for k, v in buttons.items()]
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['current'])
def current(message):
    current = helpers.find_state(-1)
    text = helpers.format_state(current)
    return bot.reply_to(message, text)
    

@bot.message_handler(commands=['get_config'])
def get_config(message):
    with open('config.json') as f:
        config = json.loads(f.read())
    config = {k:v['value'] for k, v in config.items()}
    return bot.reply_to(message, f'`{pprint.pformat(config, sort_dicts=False)}`', parse_mode='markdown')

@bot.message_handler(commands=['change_config'])
def start_change_config(message):
    with open('config.json') as f:
        config = json.loads(f.read())
    markup = {k:f"{k} ({v['value']})"  for k, v in config.items()}
    markup = init_markup(markup)
    return bot.reply_to(message, '?', reply_markup=markup)

def set_config(msg, key):
    print(msg)
    with open('config.json') as f:
        config = json.loads(f.read())
    config[key]['value'] = int(msg.text)
    config = helpers.sort_config(config)
    with open('config.json', 'w') as f:
        f.write(json.dumps(config))
    return bot.reply_to(msg, 'Config updated')

@bot.callback_query_handler(lambda callback: callback.data.startswith('max_') or callback.data.startswith('min_'))
def change_config(callback):
    msg = bot.send_message(callback.message.chat.id, f'Type value for {callback.data}:')
    bot.register_next_step_handler(msg, lambda m: set_config(m, callback.data))
    

bot.infinity_polling()