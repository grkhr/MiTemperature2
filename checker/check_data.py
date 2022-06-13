import sys
obj = sys.argv[1]
with open('data.jsonl', 'a') as f:
    f.write(obj + '\n')

from dotenv import load_dotenv
load_dotenv()

import telebot
# import pandas as pd
import json
import os
import helpers

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

with open('config.json') as f:
    config = json.loads(f.read())

last_state = helpers.find_state(-2)
current_state = helpers.find_state(-1)

# min_humidity
if current_state['humidity'] < config['min_humidity'] and last_state['humidity'] >= config['min_humidity']:
    text = f"🏜 Humidity is {current_state['humidity']}%"
    bot.send_message(os.getenv('CHAT_ID'), text)

# max_humidity
if current_state['humidity'] > config['max_humidity'] and last_state['humidity'] <= config['max_humidity']:
    text = f"💧 Humidity is {current_state['humidity']}%"
    bot.send_message(os.getenv('CHAT_ID'), text)


# min_temperature
if current_state['temperature'] < config['min_temperature'] and last_state['temperature'] >= config['min_temperature']:
    text = f"🥶 Temperature is {current_state['temperature']}°C"
    bot.send_message(os.getenv('CHAT_ID'), text)

# max_temperature
if current_state['temperature'] > config['max_temperature'] and last_state['temperature'] <= config['max_temperature']:
    text = f"🥵 Temperature is {current_state['temperature']}°C"
    bot.send_message(os.getenv('CHAT_ID'), text)

print('checked')