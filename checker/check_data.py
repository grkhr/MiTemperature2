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
import models
import db
import datetime

models.create_all()
with db.session() as sess:
    row = json.loads(obj)
    row['timestamp'] = datetime.datetime.fromtimestamp(row['timestamp'])
    sess.add(models.MHData(**row))
    sess.commit()

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

with open('config.json') as f:
    config = json.loads(f.read())

last_state = helpers.find_state(-2)
current_state = helpers.find_state(-1)

# min_humidity
if current_state['humidity'] < config['min_humidity']['value'] and last_state['humidity'] >= config['min_humidity']['value']:
    text = f"🏜 Humidity is {current_state['humidity']}%"
    bot.send_message(os.getenv('CHAT_ID'), text)

# max_humidity
if current_state['humidity'] > config['max_humidity']['value'] and last_state['humidity'] <= config['max_humidity']['value']:
    text = f"💧 Humidity is {current_state['humidity']}%"
    bot.send_message(os.getenv('CHAT_ID'), text)


# min_temperature
if current_state['temperature'] < config['min_temperature']['value'] and last_state['temperature'] >= config['min_temperature']['value']:
    text = f"🥶 Temperature is {current_state['temperature']}°C"
    bot.send_message(os.getenv('CHAT_ID'), text)

# max_temperature
if current_state['temperature'] > config['max_temperature']['value'] and last_state['temperature'] <= config['max_temperature']['value']:
    text = f"🥵 Temperature is {current_state['temperature']}°C"
    bot.send_message(os.getenv('CHAT_ID'), text)

print('checked')
