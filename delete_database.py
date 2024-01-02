import sqlite3


def clear_database():
    try:
        conn = sqlite3.connect('telegram_bot.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Users')

        cursor.execute('DELETE FROM Notes')

        conn.commit()
        print("Database deleted successfully.")

    except sqlite3.Error as e:
        print(f"Error clearing database: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    clear_database()
