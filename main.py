from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest, MessageNotModified
from config import TOKEN, logging

from weather.weather import fetch_weather_from_service
from weather.weather_api import service_weather_api
from weather.open_weather import service_open_weather


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=('start', 'help'))
async def command_start(message: types.Message):
    text = 'Меню функций: /key'
    await message.reply(text)


@dp.callback_query_handler(text='weather_api')
async def command_weather(callback_query: types.CallbackQuery):
    result = await fetch_weather_from_service(service_weather_api)
    await callback_query.message.reply(result, reply=False)


@dp.callback_query_handler(text='open_weather')
async def command_weather(callback_query: types.CallbackQuery):
    result = await fetch_weather_from_service(service_open_weather)
    await callback_query.message.reply(result, reply=False)


@dp.message_handler(commands='key')
async def send_inline_keyboard(message: types.Message):
    kb = InlineKeyboardMarkup()
    url_btn = InlineKeyboardButton('Yandex', url='https://ya.ru')
    remove_btn = InlineKeyboardButton('Удалить кнопки', callback_data='remove')
    weather_api_btn = InlineKeyboardButton('weatherapi', callback_data='weather_api')
    open_weather_btn = InlineKeyboardButton('openweather', callback_data='open_weather')
    kb.add(url_btn, weather_api_btn, open_weather_btn, remove_btn)
    await message.reply('Выбери команду:', reply_markup=kb)


@dp.callback_query_handler(text='remove')
async def remove_inline_keyboard(callback_query: types.CallbackQuery):
    await callback_query.answer('Removing kb..')
    await callback_query.message.edit_text('Выполните /key для вызова меню функций...')


@dp.callback_query_handler()
async def handle_all_callback_queries(callback_query: types.CallbackQuery):
    await callback_query.answer()


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply(message.text)


@dp.message_handler(content_types=ContentTypes.STICKER)
async def echo_sticker(message: types.Message):
    await message.reply_sticker(message.sticker.file_id, reply=False)


@dp.errors_handler(exception=MessageNotModified)
async def handler_error_message_not_modified(update: types.Update, exception):
    logging.info('Not modified update is %s', update)
    return True


@dp.errors_handler(exception=BadRequest)
async def handler_error_message_bad_request(update: types.Update, exception):
    logging.info('Message must be non-empty %s %s', update)
    return True


if __name__ == '__main__':
    executor.start_polling(dp)
