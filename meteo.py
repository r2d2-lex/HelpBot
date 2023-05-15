import asyncio
from asyncio import FIRST_COMPLETED
from http import fetch_data, Service
from config import logging


SERVICES = [
    Service('Meteo1', 'https:///?format=json', 'prognoz'),
    Service('Meteo2', 'http:///json', 'query'),
]


async def fetch_weather_fastest(timeout: int) -> str:
    weather = 'no result'
    futures = [fetch_data(s) for s in SERVICES]
    # res = await asyncio.wait(futures)
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
    res = loop.run_until_complete(fetch_weather_fastest(1))
    loop.close()
    logging.info('Result from loop: {!r}', res)


if __name__ == '__main__':
    main()
