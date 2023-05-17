from collections import OrderedDict
import asyncio
import sys
sys.path.append("..")
from aiorequest import Service
from config import logging, OPEN_WEATHER_KEY, CITY, LANG

CALLBACK = ''

weather_api_dict = OrderedDict(
    temp=dict(param=('main', 'temp'), description='Температура воздуха', sign='°C'),
    feels_like=dict(param=('main', 'feels_like'), description='Ощущается как', sign='°C'),
    pressure=dict(param=('main', 'pressure'), description='Давление',),
    wind_speed=dict(param=('wind', 'speed'), description='Скорость ветра', sign='М/с'),
    weather_state=dict(param=('weather', 0, 'description'), description='Состояние за окном',),
)

service_open_weather = Service(
    'weatherapi.com',
    f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&lang={LANG}&appid={OPEN_WEATHER_KEY}',
    CALLBACK,
    weather_api_dict,
)


def main():
    from weather import fetch_weather_from_service
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_weather_from_service(service_open_weather))
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
