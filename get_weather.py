import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *


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
