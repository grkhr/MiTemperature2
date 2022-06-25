from dotenv import load_dotenv
load_dotenv()

import telebot
import pandas as pd
import json
import pprint
import os
import socket

import helpers

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

COMMANDS = {
    'current': 'current',
    'get_config': 'get_config',
    'change_config': 'change config',
    'last_logs': 'last_logs',
    'logs_stat': 'logs_stat',
    'get_ip': 'get_ip',
}
bot.set_my_commands([telebot.types.BotCommand(k, v) for k, v in COMMANDS.items()])

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def init_markup(buttons, row_width=1):
    markup = telebot.types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [telebot.types.InlineKeyboardButton(v, callback_data=k) for k, v in buttons.items()]
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['current'])
def current(message):
    current = helpers.find_state(0)
    text = helpers.format_state(current)
    return bot.reply_to(message, text)

@bot.message_handler(commands=['last_logs'])
def get_config(message):
    ls = helpers.find_last_n_states(10)
    ls = [
        [
            helpers.stringify_ts(i['timestamp']), 
            str(i['temperature']), 
            str(i['humidity'])
        ] 
        for i in ls
    ]
    ls = '\n'.join([' '.join(i) for i in ls])
    return bot.reply_to(message, f'`{ls}`', parse_mode='markdown')

@bot.message_handler(commands=['logs_stat'])
def send_logs_stat(message):
    stat = helpers.logs_stat()
    print(stat)
    return bot.reply_to(message, f'```\n{pprint.pformat(stat, indent=1, width=1)}\n```', parse_mode='markdown')


@bot.message_handler(commands=['get_config'])
def get_config(message):
    with open('config.json') as f:
        config = json.loads(f.read())
    config = {k:v['value'] for k, v in config.items()}
    return bot.reply_to(message, f'`{pprint.pformat(config, sort_dicts=False, indent=1, width=1)}`', parse_mode='markdown')

@bot.message_handler(commands=['get_ip'])
def send_ip(message):
    ip = get_current_ip()
    return bot.reply_to(message, f'`{ip}`', parse_mode='markdown')

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