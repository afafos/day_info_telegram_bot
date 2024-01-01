import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *


bot = telebot.TeleBot(telegram_api)


def process_news_input(message, chat_id):
    try:
        country_name = message.text
        country_code = get_country_code(country_name)

        if not country_code:
            bot.send_message(chat_id, "Invalid country name. Please enter a valid country.")
            return

        news_api_url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': country_code,
            'apiKey': news_api,
        }

        response = requests.get(news_api_url, params=params)
        news_data = response.json()

        if response.status_code == 200:
            articles = news_data.get('articles', [])
            if articles:
                for article in articles[:5]:
                    title = article.get('title', 'No title')
                    url = article.get('url', 'No URL')
                    news_message = f"<b>{title}</b>\n\nRead more: {url}"
                    bot.send_message(chat_id, news_message, parse_mode="HTML")
            else:
                bot.send_message(chat_id, f"No news found for {country_name}")
        else:
            error_message = f"Error fetching news: {news_data.get('message', 'Unknown error')}"
            bot.send_message(chat_id, error_message)
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")


def get_country_code(country_name):
    country_mapping = {
        'united arab emirates': 'ae',
        'argentina': 'ar',
        'austria': 'at',
        'australia': 'au',
        'belgium': 'be',
        'bulgaria': 'bg',
        'brazil': 'br',
        'canada': 'ca',
        'switzerland': 'ch',
        'china': 'cn',
        'colombia': 'co',
        'cuba': 'cu',
        'czech republic': 'cz',
        'germany': 'de',
        'egypt': 'eg',
        'france': 'fr',
        'united kingdom': 'gb',
        'greece': 'gr',
        'hong kong': 'hk',
        'hungary': 'hu',
        'indonesia': 'id',
        'ireland': 'ie',
        'israel': 'il',
        'india': 'in',
        'italy': 'it',
        'japan': 'jp',
        'south korea': 'kr',
        'lithuania': 'lt',
        'latvia': 'lv',
        'morocco': 'ma',
        'mexico': 'mx',
        'malaysia': 'my',
        'nigeria': 'ng',
        'netherlands': 'nl',
        'norway': 'no',
        'new zealand': 'nz',
        'philippines': 'ph',
        'poland': 'pl',
        'portugal': 'pt',
        'romania': 'ro',
        'serbia': 'rs',
        'russia': 'ru',
        'saudi arabia': 'sa',
        'sweden': 'se',
        'singapore': 'sg',
        'slovenia': 'si',
        'slovakia': 'sk',
        'thailand': 'th',
        'turkey': 'tr',
        'taiwan': 'tw',
        'ukraine': 'ua',
        'united states': 'us',
        'venezuela': 've',
        'south africa': 'za'
    }

    return country_mapping.get(country_name.lower())