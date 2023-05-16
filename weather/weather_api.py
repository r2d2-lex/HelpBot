import asyncio
import sys
sys.path.append("..")
from aiorequest import fetch_data, Service
from config import logging, WEATHER_API_KEY, CITY


service = Service(
        'weatherapi.com',
        f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no',
        'current'
)


async def fetch_weather_from_weather_api() -> str:
    weather = 'Ошибка получение результата'
    result_dict = await fetch_data(service)
    try:
        weather = result_dict['temp_c']
    except KeyError:
        pass
    weather = f'Температура воздуха в {CITY}: {weather} °C'
    return weather


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_weather_from_weather_api())
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
