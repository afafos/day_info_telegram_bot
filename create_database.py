import sqlite3

conn = sqlite3.connect('telegram_bot.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        User_ID INTEGER PRIMARY KEY
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notes (
        Note_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID INTEGER,
        Date TEXT,
        Note TEXT,
        FOREIGN KEY (User_ID) REFERENCES Users (User_ID)
    )
''')

conn.commit()

conn.close()
