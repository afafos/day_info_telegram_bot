import telebot
import json
import requests
import sqlite3
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from telebot import types
from api import *

bot = telebot.TeleBot(telegram_api)


def show_notes(message):
    user_id = message.from_user.id
    date_str = message.text

    try:
        date = datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid date format. Please enter the date in the format DD-MM-YYYY.")
        return

    conn = sqlite3.connect("telegram_bot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT Note, Note_ID FROM Notes WHERE User_ID = ? AND Date = ?", (user_id, date_str))
    notes = cursor.fetchall()

    conn.close()

    if not notes:
        bot.send_message(message.chat.id, f"No notes found for the date {date_str}.")
    else:
        for index, note in enumerate(notes, start=1):
            note_text = note[0]
            note_id = note[1]

            keyboard = types.InlineKeyboardMarkup()
            delete_button = types.InlineKeyboardButton("Delete", callback_data=f"delete_note_{note_id}")
            keyboard.add(delete_button)

            bot.send_message(message.chat.id, f"<b>{index}. {note_text}</b>", reply_markup=keyboard, parse_mode="HTML")
