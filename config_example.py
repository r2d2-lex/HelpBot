import logging

TOKEN = 'TOKEN'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
CITY = 'Moscow'
WEATHER_API_KEY = 'key'
OPEN_WEATHER_KEY = 'key'
LANG = 'ru'
GOOGLE_SEARCH_IMAGE_API = 'api'
GOOGLE_SEARCH_IMAGE_CX = 'cx'

POSTGRES_HOST = '127.0.0.1'
POSTGRES_LOGIN = 'login'
POSTGRES_PASSWORD = 'pass'
BOT_DB = 'help_bot'
POSTGRES_ENGINE = 'postgresql+asyncpg'
POSTGRES_DATABASE_URI = f'{POSTGRES_ENGINE}://{POSTGRES_LOGIN}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{BOT_DB}'
