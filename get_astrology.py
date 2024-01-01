import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *

bot = telebot.TeleBot(telegram_api)


def process_zodiac_input(message, chat_id):
    signs = {
        "aries": 1,
        "taurus": 2,
        "gemini": 3,
        "cancer": 4,
        "leo": 5,
        "virgo": 6,
        "libra": 7,
        "scorpio": 8,
        "sagittarius": 9,
        "capricorn": 10,
        "aquarius": 11,
        "pisces": 12,
    }
    given_sign = message.text.lower()
    if given_sign in signs:
        URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + \
              str(signs[given_sign])

        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        container = soup.find("p")
        horoscope_text = container.text.strip()

        bot.send_message(chat_id, f"<b>Horoscope for {given_sign.capitalize()}:</b>\n\n{horoscope_text}",
                         parse_mode="HTML")
    else:
        bot.send_message(chat_id, "Invalid zodiac sign. Please enter a valid zodiac sign.")
