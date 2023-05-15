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
    data_field: list


async def fetch(session: ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()


async def fetch_data(service: Service) -> str:
    result_data = 'not found'
    logging.info(f'Starting with {service.name}')
    start = time()
    try:
        async with aiohttp.ClientSession() as session:
            json = await fetch(session, service.url)
            end = time()
            logging.info(f'Got answer from {service.name} after {end-start}')

    except CancelledError as err:
        logging.debug(f'Cancelled fetching {service.name} error: {err}')
        return 'cancelled'
    except Exception as err:
        logging.exception(f'Error with {service} error: {err}')
        return 'error'

    try:
        result_data = json[service.data_field[0]]
        if len(service.data_field) > 1:
            for index in range(1, len(service.data_field)):
                result_data = result_data[service.data_field[index]]
    except (KeyError, IndexError):
         logging.error(f'Could not get data from {json} user field {service.name}')
    return result_data
