from collections import OrderedDict
import asyncio
import sys
sys.path.append("..")
from aiorequest import Service, parse_data_from_service

CALLBACK = 'Valute'

exchange_rates = OrderedDict(
    usd=dict(param=('USD', 'Value'), description='Доллар США', sign='$'),
    eur=dict(param=('EUR', 'Value'), description='Евро', sign='€'),
    usdp=dict(param=('USD', 'Previous'), description='Предидущий курс доллара', sign='$'),
    eurp=dict(param=('EUR', 'Previous'), description='Предидущий курс евро', sign='€'),
)

service_exchange_rates = Service(
    'cbr-xml-daily.ru',
    f'https://www.cbr-xml-daily.ru/daily_json.js',
    CALLBACK,
    exchange_rates,
)


async def get_exchange_rates():
    result_str = f'Сервис: {service_exchange_rates.name}\r\nПолучение информации о курсе валют ЦБ РФ\r\n'
    result_str += await parse_data_from_service(service_exchange_rates)
    return result_str


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_exchange_rates())
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
