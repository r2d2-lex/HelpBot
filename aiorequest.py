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
    params: dict

# async def fetch_file(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 return await response.read()

async def fetch_text(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def fetch_json(session: ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return await response.json(content_type=None)


async def fetch_data(service: Service) -> str:
    result_data = 'not found'
    logging.info(f'Starting with {service.name}')
    start = time()
    try:
        async with aiohttp.ClientSession() as session:
            json = await fetch_json(session, service.url)
            end = time()
            logging.info(f'Got answer from {service.name} after {end-start}')

    except CancelledError as err:
        logging.debug(f'Cancelled fetching {service.name} error: {err}')
        return 'cancelled'
    except Exception as err:
        logging.exception(f'Error with {service} error: {err}')
        return 'error'

    try:
        if service.data_field:
            result_data = json[service.data_field]
        else:
            result_data = json
    except KeyError:
         logging.error(f'Could not get data from {json} user field {service.name}')
    return result_data


async def parse_data_from_service(service: Service) -> str:
    result_data = 'Ошибка обработки данных'
    weather_params_dict = service.params
    result_dict = await fetch_data(service)
    logging.info(result_dict)
    try:
        result_string = ''
        for key, value in weather_params_dict.items():

            params_value = value['param']
            first = True
            save_data = result_dict[params_value[0]]
            for param in params_value:
                if first:
                    first = False
                else:
                    save_data = save_data[param]
            save_data = str(save_data)

            result_string += value['description'] + ': ' + save_data + ' ' + value.get('sign', '') + '\r\n'
        result_data = result_string
    except (KeyError, TypeError, IndexError) as error:
        logging.error(f'Ошибка обработки данных: {error}')
    return result_data
