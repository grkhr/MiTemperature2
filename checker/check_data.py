from dotenv import load_dotenv
load_dotenv()

import telebot
import pandas as pd
import json
import os

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
