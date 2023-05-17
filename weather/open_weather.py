from collections import OrderedDict
import asyncio
import sys
sys.path.append("..")
from aiorequest import Service
from weather import fetch_weather_from_service
from config import logging, OPEN_WEATHER_KEY, CITY, LANG

CALLBACK = 'main'

weather_api_dict = OrderedDict(
    temp=dict(param='temp', description='Температура воздуха', sign='°C'),
    feels_like=dict(param='feels_like', description='Ощущается как', sign='°C'),
    pressure=dict(param='pressure', description='Давление',),
)

service_open_weather = Service(
    'weatherapi.com',
    f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&lang={LANG}&appid={OPEN_WEATHER_KEY}',
    CALLBACK,
    weather_api_dict,
)


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_weather_from_service(service_open_weather))
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
