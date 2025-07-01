import aiogram
import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен вашего Telegram-бота
TELEGRAM_TOKEN = '7893464712:AAEBErvxEp-_IBKeyKqsglNq5UyD77B8kG8'

# Ключ от OpenWeatherMap
WEATHER_API_KEY = '5f2ca858aa295587f0dcf31feedddf21'

# Функция для получения погоды
def get_weather(city: str) -> str:
    url = "http://api.openweathermap.org/data/2.5/weather" #https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}  
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('cod') != 200:
            return "Не удалось найти информацию о погоде для этого города."

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        return (
            f"🌤 Погода в городе {city}:\n"
            f"Описание: {weather}\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
    except Exception as e:
        return f"Ошибка при получении данных: {e}"

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Напиши название города, и я скажу тебе погоду.")


# Обработчик текстовых сообщений
@dp.message(F.text)
async def weather_handler(message: Message):
    city = message.text.strip()
    weather_info = get_weather(city)
    await message.answer(weather_info)

# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())