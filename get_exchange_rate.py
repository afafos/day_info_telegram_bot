import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *

bot = telebot.TeleBot(telegram_api)


def get_and_display_inverse_rates(api_key, base_currency, selected_currencies, chat_id):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data['result'] == 'success':
            rates = data['conversion_rates']

            if rates:
                rates_message = "<b>Exchange rates:</b>\n\n"
                for currency in selected_currencies:
                    if currency in rates:
                        rate = rates[currency]
                        inverse_rate = 1 / rate
                        inverse_rate_formatted = '{:.2f}'.format(inverse_rate)
                        rates_message += f"<b>{currency}:</b> {inverse_rate_formatted}\n"
                    else:
                        rates_message += f"<b>{currency}:</b> Exchange rate not available.\n"

                bot.send_message(chat_id, rates_message, parse_mode="HTML")
            else:
                bot.send_message(chat_id, "Error: No exchange rates available.")
        else:
            bot.send_message(chat_id, f"Error: {data['error']} - {data['info']}")

    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {e}")


def process_currency_input(message, chat_id):
    base_currency = message.text.upper()
    if base_currency.isalpha():
        selected_currencies = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'CAD', 'AUD', 'CNY', 'SEK', 'NZD']
        get_and_display_inverse_rates(exchange_api, base_currency, selected_currencies, chat_id)
    else:
        bot.send_message(chat_id, "Invalid currency code. Please enter a valid 3-letter currency code.")
