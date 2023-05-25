from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentTypes, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import BadRequest, MessageNotModified
from config import TOKEN, logging
from utils import get_keyboard

from weather.weather_api import get_weather_from_weather_api
from weather.open_weather import get_weather_from_open_weather
from erates.cbr_xml_daily import get_exchange_rates

from search_image.google_search_image import google_search_image, google_next_search, google_new_search


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=('start', 'help'))
async def command_start(message: types.Message):
    text = 'Меню функций: /key'
    await message.reply(text, reply_markup=get_keyboard())


@dp.callback_query_handler(text='weather_api')
async def command_weather(callback_query: types.CallbackQuery):
    result = await get_weather_from_weather_api()
    await callback_query.message.reply(result, reply_markup=get_keyboard())
    await callback_query.answer()


@dp.message_handler(commands='img_next')
async def search_image_next(message: types.Message):
    google_next_search(message.from_user.id)
    await send_image(message)
    await message.reply('Следующие сообщения', reply_markup=get_keyboard())


@dp.message_handler(commands='img')
async def search_image(message: types.Message):
    google_new_search(message.from_user.id)
    await send_image(message)
    await message.reply('Загрузить ещё? /img_next:', reply_markup=get_keyboard())


async def send_image(message: types.Message):
    search_arg = message.get_args()
    logging.debug(f'Аргументы: {search_arg}')
    for image in google_search_image(search_arg, message.from_user.id, 5):
        await bot.send_photo(chat_id=message.chat.id, photo=image)


@dp.callback_query_handler(text='open_weather')
async def command_weather(callback_query: types.CallbackQuery):
    result = await get_weather_from_open_weather()
    await callback_query.message.reply(result, reply_markup=get_keyboard())
    await callback_query.answer()


@dp.callback_query_handler(text='exchange_rates')
async def exchange_rates(callback_query: types.CallbackQuery):
    result = await get_exchange_rates()
    await callback_query.message.reply(result, reply_markup=get_keyboard())
    await callback_query.answer()


@dp.message_handler(commands='key')
async def send_inline_keyboard(message: types.Message):
    await message.reply('Выбери команду:', reply_markup=get_keyboard())


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
