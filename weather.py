from pyowm import OWM
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError
import TOKENS

config_dict = get_default_config()
config_dict['language'] = 'ru'


def weather_info_api(place):
    owm = OWM(TOKENS.OWM)
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(place)
        w = observation.weather
        temperature = int(w.temperature('celsius')['temp'])
        wind = w.wind()['speed']
        humidity = w.humidity
        return (f'''
В городе {place}: {w.detailed_status}.
Температура сейчас: {temperature} градусов.
Скорость ветра: {wind} м/с.
Влажность: {humidity} %.
''')

    except NotFoundError:
        return (f'Не найдено место: {place}')
