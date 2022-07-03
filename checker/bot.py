from dotenv import load_dotenv
load_dotenv()

import telebot
import pandas as pd
import json
import pprint
import os
from miio import chuangmi_plug
import socket
import time

import helpers

from functools import wraps


KNOWN_CHAT_IDS = [104327226, 149021256]


def private_access():
    """
    Restrict access to the command to users allowed by the is_known_username function.
    """
    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            if message.chat.id in KNOWN_CHAT_IDS:
                return f(message, *args, **kwargs)
            else:
                bot.reply_to(message, text='Who are you?  Keep on walking...')

        return f_restrict  # true decorator

    return deco_restrict


bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

COMMANDS = {
    'current': 'current',
    'get_config': 'get_config',
    'change_config': 'change config',
    # 'last_logs': 'last_logs',
    'logs_stat': 'logs_stat',
    'get_ip': 'get_ip',
    'plug_on': 'plug_on',
    'plug_off': 'plug_off',
    'plug_status': 'plug_status',
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
@private_access()
def current(message):
    send = []
    objs = helpers.get_devices()
    for obj in objs:
        current = helpers.find_state(0, obj.sensorname)
        text = obj.sensortitle.upper() + '\n' + helpers.format_state(current)
        send.append(text)
    return bot.reply_to(message, '\n\n'.join(send))

# @bot.message_handler(commands=['last_logs'])
# @private_access()
# def get_config(message):
#     ls = helpers.find_last_n_states(10)
#     ls = [
#         [
#             helpers.stringify_ts(i['timestamp']), 
#             str(i['temperature']), 
#             str(i['humidity'])
#         ] 
#         for i in ls
#     ]
#     ls = '\n'.join([' '.join(i) for i in ls])
#     return bot.reply_to(message, f'`{ls}`', parse_mode='markdown')

@bot.message_handler(commands=['logs_stat'])
@private_access()
def send_logs_stat(message):
    stat = helpers.logs_stat()
    print(stat)
    return bot.reply_to(message, f'```\n{pprint.pformat(stat, indent=1, width=1)}\n```', parse_mode='markdown')


@bot.message_handler(commands=['get_config'])
@private_access()
def get_config(message):
    with open('config.json') as f:
        config = json.loads(f.read())
    config = {k:v['value'] for k, v in config.items()}
    return bot.reply_to(message, f'`{pprint.pformat(config, sort_dicts=False, indent=1, width=1)}`', parse_mode='markdown')

@bot.message_handler(commands=['get_ip'])
@private_access()
def send_ip(message):
    ip = get_current_ip()
    return bot.reply_to(message, f'`{ip}`', parse_mode='markdown')


@bot.message_handler(commands=['plug_on', 'plug_off', 'plug_status'])
@private_access()
def plug_controller(message):
    plug = chuangmi_plug.ChuangmiPlug(os.getenv('PLUG_IP'), os.getenv('PLUG_TOKEN'))
    if message.text == '/plug_on':
        plug.on()
        return bot.reply_to(message, 'Plug on')
    if message.text == '/plug_off':
        plug.off()
        return bot.reply_to(message, 'Plug off')
    if message.text == '/plug_status':
        return bot.reply_to(message, 'Plug status:\n is_on ' + str(plug.status().is_on))
    return

@bot.message_handler(commands=['change_config'])
@private_access()
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
    
while True:
    try:
        print('trying poll...')
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(20)
