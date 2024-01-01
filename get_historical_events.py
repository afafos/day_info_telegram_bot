import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *


bot = telebot.TeleBot(telegram_api)


def send_historical_events(chat_id):
    today = datetime.now()
    day = today.day
    month = today.month
    api_url = 'https://api.api-ninjas.com/v1/historicalevents?day={}&month={}'.format(day, month)
    response = requests.get(api_url, headers={'X-Api-Key': historical_events_api})

    if response.status_code == requests.codes.ok:
        historical_events = response.json()
        events_text = "\n\n".join([f"<b>{event['day']}-{event['month']}-{event['year']}:</b> {event['event']}" for event in historical_events])
        bot.send_message(chat_id, f"<b>Historical Events for {today.strftime('%B %d')}:</b>\n\n{events_text}", parse_mode="HTML")
    else:
        bot.send_message(chat_id, f"Error fetching historical events: {response.status_code}")
