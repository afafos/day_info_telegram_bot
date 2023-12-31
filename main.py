import telebot
import json
import requests
from datetime import datetime
from telebot import types
from datetime import datetime, timedelta
from api import *


OpWeather_api = openweather_api

bot = telebot.TeleBot(telegram_api)


def get_current_weather_info(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OpWeather_api}'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return parse_weather_data(weather_data)
    else:
        return "Failed to fetch current weather information. Please try again later."


def get_forecast_info(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={OpWeather_api}'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return parse_forecast_data(weather_data)
    else:
        return "Failed to fetch weather forecast information. Please try again later."


def parse_weather_data(weather_data):
    main_weather = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description']
    temperature_kelvin = weather_data['main']['temp']
    feels_like_kelvin = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']

    temperature_celsius = temperature_kelvin - 273.15
    feels_like_celsius = feels_like_kelvin - 273.15

    weather_message = (
        f"Weather: {main_weather}\n"
        f"Description: {description}\n"
        f"Temperature: {temperature_celsius:.2f}°C\n"
        f"Feels Like: {feels_like_celsius:.2f}°C\n"
        f"Humidity: {humidity}%\n"
        f"Wind Speed: {wind_speed} m/s"
    )

    return weather_message


def parse_forecast_data(weather_data):
    forecast_list = weather_data['list']

    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%d-%m-%Y')

    forecast_messages = []
    for forecast in forecast_list:
        timestamp = forecast['dt']
        forecast_date = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

        if forecast_date[:10] != tomorrow_date:
            continue

        main_weather = forecast['weather'][0]['main']
        description = forecast['weather'][0]['description']
        temperature_kelvin = forecast['main']['temp']
        humidity = forecast['main']['humidity']
        wind_speed = forecast['wind']['speed']

        temperature_celsius = temperature_kelvin - 273.15

        forecast_message = (
            f"Forecast for {forecast_date}\n"
            f"Weather: {main_weather}\n"
            f"Description: {description}\n"
            f"Temperature: {temperature_celsius:.2f}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s\n"
        )
        forecast_messages.append(forecast_message)

    return "\n\n".join(forecast_messages)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! Enter the /find command to get information about the current day!")


@bot.message_handler(commands=['find'])
def handle_find(message):
    today_date = datetime.now().strftime("%d-%m-%Y")

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Get Weather Forecast", callback_data="weather_forecast")
    markup.add(button)

    bot.send_message(message.chat.id, f"Today's date: {today_date}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "weather_forecast":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        bot.send_message(call.message.chat.id, "Please share your location:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def handle_text(message):
    try:
        coordinates = [float(coord) for coord in message.text.split(',')]
        if len(coordinates) == 2:
            user_id = message.from_user.id
            coordinates_dict = {"user_coordinates": {"latitude": coordinates[0], "longitude": coordinates[1]}}
            with open(f"user_{user_id}_coordinates.json", "w") as json_file:
                json.dump(coordinates_dict, json_file)

            current_weather_info = get_current_weather_info(coordinates[0], coordinates[1])
            bot.send_message(message.chat.id, "Current Weather:\n\n" + current_weather_info)

            forecast_info = get_forecast_info(coordinates[0], coordinates[1])
            bot.send_message(message.chat.id, "Weather Forecast:\n\n" + forecast_info)
        else:
            bot.send_message(message.chat.id,
                             "Invalid coordinates format. Please enter latitude and longitude separated by a comma.")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid coordinates format. Please enter valid numeric values.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
