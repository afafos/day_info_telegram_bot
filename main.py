import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *
from get_weather import *
from get_astrology import *
from get_exchange_rate import *
from get_news import *
from get_quote import *

bot = telebot.TeleBot(telegram_api)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! Enter the /find command to get information about the current day!")


@bot.message_handler(commands=['find'])
def handle_find(message):
    today_date = datetime.now().strftime("%d-%m-%Y")

    random_quote = get_random_quote()

    markup = telebot.types.InlineKeyboardMarkup()
    button_forecast = telebot.types.InlineKeyboardButton(text="Get Weather Forecast", callback_data="weather_forecast")
    button_astro = telebot.types.InlineKeyboardButton(text="Get an Astrological Forecast",
                                                      callback_data="astro_forecast")
    button_exchange_rate = telebot.types.InlineKeyboardButton(text="Get Exchange Rate", callback_data="exchange_rate")
    button_news = telebot.types.InlineKeyboardButton(text="Get the latest news", callback_data="news")

    markup.add(button_forecast)
    markup.add(button_astro)
    markup.add(button_exchange_rate)
    markup.add(button_news)

    bot.send_message(message.chat.id, f"<b>Today's date:</b> {today_date}\n\n{random_quote}", reply_markup=markup, parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "weather_forecast":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        bot.send_message(call.message.chat.id, "Please share your location:", reply_markup=keyboard)
    elif call.data == "astro_forecast":
        bot.send_message(call.message.chat.id, "Please enter your zodiac sign:")
        bot.register_next_step_handler(call.message, process_zodiac_input, call.message.chat.id)
    elif call.data == "exchange_rate":
        bot.send_message(call.message.chat.id, "Please enter the base currency:")
        bot.register_next_step_handler(call.message, process_currency_input, call.message.chat.id)
    elif call.data == "news":
        bot.send_message(call.message.chat.id, "Please enter the country:")
        bot.register_next_step_handler(call.message, process_news_input, call.message.chat.id)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_text(message):
    try:
        address = message.text
        coordinates = get_coordinates_by_address(address)

        if coordinates:
            user_id = message.from_user.id
            coordinates_dict = {"user_coordinates": {"latitude": coordinates[0], "longitude": coordinates[1]}}
            with open(f"user_{user_id}.json", "w") as json_file:
                json.dump(coordinates_dict, json_file)

            current_weather_info = get_current_weather_info(coordinates[0], coordinates[1])
            current_weather_info_ai = get_cur_weather_description(current_weather_info)
            bot.send_message(message.chat.id, "<b>Current Weather:</b>\n\n" + current_weather_info_ai,
                             parse_mode="HTML")

            forecast_info = get_forecast_info(coordinates[0], coordinates[1])
            forecast_info_ai = get_forecast_description(forecast_info)
            bot.send_message(message.chat.id, "<b>Weather Forecast:</b>\n\n" + forecast_info_ai, parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, f"Failed to get coordinates for the location: {address}")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid coordinates format. Please enter valid numeric values.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
