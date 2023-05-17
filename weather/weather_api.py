from collections import OrderedDict
import asyncio
import sys
sys.path.append("..")
from aiorequest import Service, parse_data_from_service
from config import logging, WEATHER_API_KEY, CITY


weather_api_dict = OrderedDict(
    temp_c=dict(param=('temp_c',), description='Температура воздуха', sign='°C'),
    feels_like_c=dict(param=('feelslike_c',), description='Ощущается как', sign='°C'),
    wind_kph=dict(param=('wind_kph',), description='Скорость ветра', sign='Км/ч'),
    last_updated=dict(param=('last_updated',), description='Данные получены'),
)

service_weather_api = Service(
    'weatherapi.com',
    f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no',
    'current',
    weather_api_dict,
)


async def get_weather_from_weather_api():
    result_str = f'Сервис: {service_weather_api.name}\r\nПолучение информации о погоде в {CITY}:\r\n'
    result_str += await parse_data_from_service(service_weather_api)
    return result_str


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_weather_from_weather_api())
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
