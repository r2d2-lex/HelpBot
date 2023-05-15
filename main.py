from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.handler import SkipHandler
from aiogram.types import ContentTypes, \
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import TelegramAPIError, MessageNotModified
from config import TOKEN, logging


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


def is_reply(message: types.Message):
    if message.reply_to_message:
        return {'r_msg': message.reply_to_message}


@dp.message_handler(commands=('start', 'help'))
async def command_start(message: types.Message):
    text = 'Hello'
    if message.text.startswith('/help'):
        text += ' help'
    text += '!'
    await message.reply(text)


@dp.message_handler(commands='key')
async def send_inline_keyboard(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(*(InlineKeyboardButton(text, callback_data=text.lower()) for text in ('YES','NO')))
    url_btn = InlineKeyboardButton('NOTES', url='https://ya.ru')
    remove_btn = InlineKeyboardButton('remove kb', callback_data='remove')
    kb.add(remove_btn, url_btn)
    await message.reply('Buttons here:', reply_markup=kb)


@dp.message_handler(is_reply)
async def answer_reply_message(message: types.Message, r_msg: types.Message):
    logging.info('r_msg = %s', r_msg)
    text = 'Is reply to '
    if r_msg.text:
        text += f'"{r_msg.text}"'
    else:
        text += f'a {r_msg.content_type}'
    await message.reply(text)


@dp.callback_query_handler(text='yes')
async def handle_callback_query_yes(callback_query: types.CallbackQuery):
    await callback_query.answer('Accepted!')


@dp.callback_query_handler(text='no')
async def handle_callback_query_no(callback_query: types.CallbackQuery):
    await callback_query.answer('Why not?', show_alert=True)


@dp.callback_query_handler(text='remove')
async def remove_inline_keyboard(callback_query: types.CallbackQuery):
    # await bot.edit_message_text(callback_query.from_user.id)
    # await bot.edit_message_text(callback_query.message.from_user)
    await callback_query.answer('Removing kb..')
    await callback_query.message.edit_text('Buttons were here...')
    await callback_query.message.edit_text('Buttons were here...')


@dp.callback_query_handler()
async def handle_all_callback_queries(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    await callback_query.answer()


@dp.message_handler(commands='xkey')
async def send_markup(message: types.Message):
    kb = ReplyKeyboardMarkup()
    kb.add(*(KeyboardButton(text) for text in ('YES', 'NO', '/remove')))
    ask_phone = KeyboardButton('Send phone number', request_contact=True)
    kb.add(ask_phone)
    await message.reply('Kb is here:', reply_markup=kb)


@dp.message_handler(user_id=777)
async def welcome(message: types.Message):
    await message.reply('Hello 777!')
    raise SkipHandler


@dp.message_handler(text='remove')
@dp.message_handler(commands='remove')
async def remove_markup(message: types.Message):
    await message.reply('Removed...', reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(message.chat.id, 'Removed...', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands='help')
# async def command_help(message: types.Message):
#     await message.reply('Hello help!')


@dp.message_handler()
async def echo_message(message: types.Message):
    # await bot.send_message(message.chat.id, message.text)
    await message.reply(message.text)


@dp.message_handler(content_types=ContentTypes.STICKER)
async def echo_sticker(message: types.Message):
    # await bot.send_sticker(message.chat.id, message.sticker.file_id)
    await message.reply_sticker(message.sticker.file_id, reply=False)


@dp.errors_handler(exception=MessageNotModified)
async def handler_error_message_not_modified(update: types.Update, e):
    logging.info('Not modified update is %s', update)
    return True


# @dp.errors_handler(exception=TelegramAPIError)
# async def handler_telegram_api_error(update, e):
#     logging.error('Unexpected error!', exc_info=True)
#     return True


if __name__ == '__main__':
    executor.start_polling(dp)
