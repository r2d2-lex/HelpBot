import logging
from aiorequest import Service, fetch_data


async def fetch_weather_from_service(service: Service) -> str:
    weather = 'Ошибка получение результата'
    weather_params_dict = service.params
    result_dict = await fetch_data(service)
    logging.info(result_dict)
    try:
        weather_string = ''
        for key, value in weather_params_dict.items():
            param_value = result_dict[value['param']]
            param_value = str(param_value)
            weather_string += value['description'] + ': ' + param_value + ' ' + value.get('sign', '') + '\r\n'
        weather = weather_string
    except (KeyError, TypeError) as error:
        logging.error(f'Ошибка получения данных: {error}')
    return weather
