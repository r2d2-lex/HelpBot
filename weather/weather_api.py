from collections import OrderedDict
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

weather_dict = OrderedDict(
    temp_c=dict(param='temp_c', description='Температура воздуха', sign='°C'),
    feels_like_c=dict(param='feelslike_c', description='Ощущается как', sign='°C'),
    wind_kph=dict(param='wind_kph', description='Скорость ветра', sign='Км/ч'),
    last_updated=dict(param='last_updated', description='Данные получены'),
)


async def fetch_weather_from_weather_api() -> str:
    weather = 'Ошибка получение результата'
    result_dict = await fetch_data(service)
    logging.info(result_dict)
    try:
        weather_string = ''
        for key, value in weather_dict.items():
            param_value = result_dict[value['param']]
            param_value = str(param_value)
            weather_string += value['description'] + ': ' + param_value + ' ' + value.get('sign', '') + '\r\n'
        weather = weather_string
    except (KeyError, TypeError) as error:
        logging.error(f'Ошибка получения данных: {error}')
    return weather


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_weather_from_weather_api())
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
