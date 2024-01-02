import telebot
import telebot
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from telebot import types
from api import *

bot = telebot.TeleBot(telegram_api)


def save_note(message, user_id):
    note = message.text
    date = datetime.now().strftime("%d-%m-%Y")

    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO Users (User_ID) VALUES (?)", (user_id,))

    cursor.execute("SELECT User_ID FROM Users WHERE User_ID = ?", (user_id,))
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO Notes (User_ID, Date, Note) VALUES (?, ?, ?)", (user_id, date, note))

    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, "Note saved successfully!")