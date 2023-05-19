from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard():
    kb = InlineKeyboardMarkup()
    url_btn = InlineKeyboardButton('Yandex', url='https://ya.ru')
    remove_btn = InlineKeyboardButton('Удалить кнопки', callback_data='remove')
    weather_api_btn = InlineKeyboardButton('weatherapi', callback_data='weather_api')
    open_weather_btn = InlineKeyboardButton('openweather', callback_data='open_weather')
    kb.add(url_btn, weather_api_btn, open_weather_btn, remove_btn)
    return kb