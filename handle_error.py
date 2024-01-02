import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *


def handle_error(chat_id, error_message):
    print(error_message)
    bot.send_message(chat_id, error_message)
