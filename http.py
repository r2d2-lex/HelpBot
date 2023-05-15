import aiohttp
from asyncio import CancelledError
from aiohttp import ClientSession
from time import time
from dataclasses import dataclass
from config import logging


@dataclass
class Service:
    name: str
    url: str
    data_field: str


async def fetch(session: ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()


async def fetch_data(service: Service) -> str:
    result_data = 'not found'
    logging.info('Starting with {}', service.name)
    start = time()
    try:
        async with aiohttp.ClientSession() as session:
            json = await fetch(session, service.url)
            end = time()
            logging.info('Got answer from {} after {:3f}', service.name, end-start)

    except CancelledError as err:
        logging.debug('Cancelled fetching {!r}', service.name, exc_info=err)
        # logging.opt(exception=err).debug('Cancelled fetching {!r}', service.name)
        return 'cancelled'
    except Exception as err:
        logging.exception('Error with {}', service)
        return 'error'

    try:
        result_data = json[service.data_field]
    except KeyError:
         logging.exception('Could not get data from {} user field {}', json, service.name)
    return result_data
