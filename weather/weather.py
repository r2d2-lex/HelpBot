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

            params_value = value['param']
            first = True
            save_data = result_dict[params_value[0]]
            for param in params_value:
                if first:
                    first = False
                else:
                    save_data = save_data[param]
            save_data = str(save_data)

            weather_string += value['description'] + ': ' + save_data + ' ' + value.get('sign', '') + '\r\n'
        weather = weather_string
    except (KeyError, TypeError, IndexError) as error:
        logging.error(f'Ошибка получения данных: {error}')
    return weather
