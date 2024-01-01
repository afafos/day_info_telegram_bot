import telebot
import json
import requests
from datetime import datetime, timedelta
from api import *
from bs4 import BeautifulSoup

openweather_api = opweather_api
mapquest_api = mapq_api
telegram_api = tg_api
deepai_api = ai_api

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

        bot.send_message(chat_id, f"Horoscope for {given_sign.capitalize()}:\n\n{horoscope_text}")
    else:
        bot.send_message(chat_id, "Invalid zodiac sign. Please enter a valid zodiac sign.")


def get_cur_weather_description(current_weather_info):
    payload = {
        'text': 'Write a description, saving all weather data without dates and times. {}'.format(current_weather_info)
    }

    headers = {
        'api-key': deepai_api
    }

    response = requests.post("https://api.deepai.org/api/text-generator", data=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        brief_description = result.get('output', 'No description available')
        return brief_description
    else:
        return 'Failed to get description'


def get_forecast_description(forecast_info):
    payload = {
        'text': 'Write a description saving all the weather data without dates and times. {}'.format(forecast_info)
    }

    headers = {
        'api-key': deepai_api
    }

    response = requests.post("https://api.deepai.org/api/text-generator", data=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        brief_description = result.get('output', 'No description available')
        return brief_description
    else:
        return 'Failed to get description'


def get_coordinates_by_address(address):
    base_url = "http://www.mapquestapi.com/geocoding/v1/address"
    params = {"key": mapquest_api, "location": address}
    response = requests.get(base_url, params=params)
    data1 = response.json()

    if data1["results"]:
        location = data1["results"][0]["locations"][0]
        lat = location["latLng"]["lat"]
        lng = location["latLng"]["lng"]
        return lat, lng
    else:
        return None


def get_current_weather_info(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={openweather_api}'
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return parse_weather_data(weather_data)
    else:
        return "Failed to fetch current weather information. Please try again later."


def get_forecast_info(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={openweather_api}'
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

    markup = telebot.types.InlineKeyboardMarkup()
    button_forecast = telebot.types.InlineKeyboardButton(text="Get Weather Forecast", callback_data="weather_forecast")
    button_astro = telebot.types.InlineKeyboardButton(text="Get an Astrological Forecast",
                                                      callback_data="astro_forecast")
    markup.add(button_forecast, button_astro)

    bot.send_message(message.chat.id, f"Today's date: {today_date}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "weather_forecast":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        bot.send_message(call.message.chat.id, "Please share your location:", reply_markup=keyboard)
    elif call.data == "astro_forecast":
        bot.send_message(call.message.chat.id, "Please enter your zodiac sign:")
        bot.register_next_step_handler(call.message, process_zodiac_input, call.message.chat.id)


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
            bot.send_message(message.chat.id, "Current Weather:\n\n" + current_weather_info_ai)

            forecast_info = get_forecast_info(coordinates[0], coordinates[1])
            forecast_info_ai = get_forecast_description(forecast_info)
            bot.send_message(message.chat.id, "Weather Forecast:\n\n" + forecast_info_ai)
        else:
            bot.send_message(message.chat.id, f"Failed to get coordinates for the location: {address}")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid coordinates format. Please enter valid numeric values.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
