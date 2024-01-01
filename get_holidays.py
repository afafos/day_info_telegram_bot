import telebot
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from api import *

bot = telebot.TeleBot(telegram_api)


def send_holidays(chat_id):
    country_dict = {
        "AD": "Andorra",
        "AL": "Albania",
        "AR": "Argentina",
        "AT": "Austria",
        "AU": "Australia",
        "AX": "Åland Islands",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "BE": "Belgium",
        "BG": "Bulgaria",
        "BJ": "Benin",
        "BO": "Bolivia",
        "BR": "Brazil",
        "BS": "Bahamas",
        "BW": "Botswana",
        "BY": "Belarus",
        "BZ": "Belize",
        "CA": "Canada",
        "CH": "Switzerland",
        "CL": "Chile",
        "CN": "China",
        "CO": "Colombia",
        "CR": "Costa Rica",
        "CU": "Cuba",
        "CY": "Cyprus",
        "CZ": "Czechia",
        "DE": "Germany",
        "DK": "Denmark",
        "DO": "Dominican Republic",
        "EC": "Ecuador",
        "EE": "Estonia",
        "EG": "Egypt",
        "ES": "Spain",
        "FI": "Finland",
        "FO": "Faroe Islands",
        "FR": "France",
        "GA": "Gabon",
        "GB": "United Kingdom",
        "GD": "Grenada",
        "GG": "Guernsey",
        "GI": "Gibraltar",
        "GL": "Greenland",
        "GM": "Gambia",
        "GR": "Greece",
        "GT": "Guatemala",
        "GY": "Guyana",
        "HN": "Honduras",
        "HR": "Croatia",
        "HT": "Haiti",
        "HU": "Hungary",
        "ID": "Indonesia",
        "IE": "Ireland",
        "IM": "Isle of Man",
        "IS": "Iceland",
        "IT": "Italy",
        "JE": "Jersey",
        "JM": "Jamaica",
        "JP": "Japan",
        "KR": "South Korea",
        "LI": "Liechtenstein",
        "LS": "Lesotho",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LV": "Latvia",
        "MA": "Morocco",
        "MC": "Monaco",
        "MD": "Moldova",
        "ME": "Montenegro",
        "MG": "Madagascar",
        "MK": "North Macedonia",
        "MN": "Mongolia",
        "MS": "Montserrat",
        "MT": "Malta",
        "MX": "Mexico",
        "MZ": "Mozambique",
        "NA": "Namibia",
        "NE": "Niger",
        "NG": "Nigeria",
        "NI": "Nicaragua",
        "NL": "Netherlands",
        "NO": "Norway",
        "NZ": "New Zealand",
        "PA": "Panama",
        "PE": "Peru",
        "PG": "Papua New Guinea",
        "PL": "Poland",
        "PR": "Puerto Rico",
        "PT": "Portugal",
        "PY": "Paraguay",
        "RO": "Romania",
        "RS": "Serbia",
        "RU": "Russia",
        "SE": "Sweden",
        "SG": "Singapore",
        "SI": "Slovenia",
        "SJ": "Svalbard and Jan Mayen",
        "SK": "Slovakia",
        "SM": "San Marino",
        "SR": "Suriname",
        "SV": "El Salvador",
        "TN": "Tunisia",
        "TR": "Turkey",
        "UA": "Ukraine",
        "US": "United States",
        "UY": "Uruguay",
        "VA": "Vatican City",
        "VE": "Venezuela",
        "VN": "Vietnam",
        "ZA": "South Africa",
        "ZW": "Zimbabwe",
    }

    url = "https://date.nager.at/api/v3/NextPublicHolidaysWorldwide"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        handle_error(chat_id, f"Http Error: {errh}")
        return
    except requests.exceptions.ConnectionError as errc:
        handle_error(chat_id, f"Error Connecting: {errc}")
        return
    except requests.exceptions.Timeout as errt:
        handle_error(chat_id, f"Timeout Error: {errt}")
        return
    except requests.exceptions.RequestException as err:
        handle_error(chat_id, f"OOps: Something went wrong {err}")
        return

    data = response.json()

    today_date = datetime.now().date()

    if isinstance(data, list):
        holidays_message = ""
        for holiday in data:
            holiday_date = datetime.strptime(holiday['date'], "%Y-%m-%d").date()
            if holiday_date == today_date:
                country_name = country_dict.get(holiday['countryCode'], "Unknown")
                holidays_message += f"<b>Holiday:</b> {holiday['name']}\n<b>Country:</b> {country_name}\n\n"

        if holidays_message:
            bot.send_message(chat_id, holidays_message, parse_mode='HTML')
    else:
        handle_error(chat_id, "Invalid data format. The list was expected.")