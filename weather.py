import asyncio
from asyncio import FIRST_COMPLETED
from aiorequest import fetch_data, Service
from config import logging, WEATHER_API_KEY, CITY


SERVICES = [
    Service(
        'weatherapi.com',
        f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no',
        ['current', 'temp_c'],
    ),
]


async def fetch_weather_fastest(timeout: int) -> str:
    weather = 'no result'
    futures = [asyncio.create_task(fetch_data(s)) for s in SERVICES]
    done, pending = await asyncio.wait(
        futures,
        timeout=timeout,
        return_when=FIRST_COMPLETED,
    )

    for fut in pending:
        fut.cancel()

    for fut in done:
        weather = fut.result()
        break
    else:
        logging.warning('Could not fetch any results in {} s', timeout)
    return weather


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch_weather_fastest(1))
    loop.close()
    logging.info(f'Температура воздуха в {CITY}: {result} °C')


if __name__ == '__main__':
    main()
