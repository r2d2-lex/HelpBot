import datetime
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Yandex', url='https://ya.ru')
    builder.button(text='Удалить кнопки', callback_data='remove')
    builder.button(text='weatherapi', callback_data='weather_api')
    builder.button(text='openweather', callback_data='open_weather')
    builder.button(text='Курсы валют', callback_data='exchange_rates')
    builder.button(text='Habr новости', callback_data='habr_news')
    builder.adjust(2, 3)
    return builder.as_markup()

def get_date_time(template):
    return datetime.datetime.now(tz=datetime.timezone.utc).strftime(template)
