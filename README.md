# DayWiseBot

This project implements a Telegram bot that provides various functionalities including weather information, astrology forecasts,
exchange rates, latest news, historical events, holidays and note-taking capabilities for the current day.

## Getting Started

### Prerequisites

Before running the bot, you'll need API keys for the following services:

- Telegram API
- OpenWeather API
- DeepAI API
- ExchangeRate API
- MapQuest API
- News API
- Historical Events API

### Installation

**Install the required dependencies.**
   ```
   pip install -r requirements.txt
   ```

### Configuration

**In the api.py file, replace the placeholder values for API keys with your actual keys:**

   ```
   telegram_api = 'telegram_api_key'
   openweather_api = 'openweather_api_key'
   mapquest_api = 'mapquest_api_key'
   deepai_api = 'deepai_api_key'
   exchange_api = 'exchange_api_key'
   news_api = 'news_api_key'
   historical_events_api = 'historical_events_api_key'
   ```
### Usage   
   
**Start the bot by running the main.py script:**

```
python main.py
```
## Functionality

**Commands:**  
`/start` - Initiates the conversation with the bot. Displays a welcome message and provides options to write or show notes.  
`/find`  - Provides information about the current day, including a random quote. Presents interactive buttons for various functionalities.  

**Interactive buttons:**  
* `Write Note` -  Allows the user to input a note.
* `Show Notes` - Displays saved notes for a certain date.
* `Get Weather Forecast` - Requests the user's location to provide current weather and a forecast.
* `Get an Astrological Forecast` - Prompts the user to enter his/her zodiac sign. Fetches and sends the daily horoscope for the specified sign.
* `Get Exchange Rate` - Asks the user to input a base currency code. Retrieves and displays exchange rates for popular currencies.
* `Get the latest news` - Requests the user to enter a country name. Retrieves and sends the latest news headlines for the specific country.
* `Get information about this day in history` - Fetches historical events for the current day.
* `Get holidays` - Retrieves public holidays worldwide.

## Additional Scripts

- **create_database.py:**
  This script initializes the SQLite database for storing user information and notes.
- **delete_database.py:**
  This script clears all data from the SQLite database.
- **get_astrology.py:**
  Fetches and sends daily horoscope information based on the user's zodiac sign.
- **get_exchange_rate.py:**
  Retrieves and displays exchange rates for popular currencies.
- **get_historical_events.py:**
  Fetches historical events for the current day.
- **get_holidays.py:**
  Fetches public holidays worldwide.
- **get_news.py:**
  Sends the latest news headlines based on the user's specified country.
- **get_quote.py:**
  Fetches a random quote from the quotable.io API.
- **get_weather.py:**
  Provides current weather information and a weather forecast based on the user's location.
- **handle_error.py:**
  Handles errors and sends error messages to the user.
- **main.py:**
  The main script that sets up the Telegram bot, handles user interactions and dispatches requests to varius modules.
- **save_note.py:**
  Handles the user's request to save note storing it in the SQLite database.
- **show_note.py:**
  Displays saved notes for a specified date.
