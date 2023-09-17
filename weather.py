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
        emoji = set_emoji_status(w.detailed_status)
        wind_emoji = set_wind_emoji(wind)
        temperature_emoji = set_emoji_temperature(temperature)
        humidity_emoji = set_emoji_humidity(humidity)

        return (f'''
В городе {place}: {w.detailed_status} {emoji}
Температура сейчас: {temperature} градусов {temperature_emoji}
Скорость ветра: {wind} м/с {wind_emoji}
Влажность: {humidity} % {humidity_emoji}
''')

    except NotFoundError:
        return (f'Не найдено место: {place}')


def set_emoji_status(status):
    emoji = ""
    if status == "ясно":
        emoji = "☀️"
    elif status == "пасмурно":
        emoji = "🌤️"
    elif status == "рассеянные облака":
        emoji = "⛅"
    elif status == "переменная облачность" or status == "облачно с прояснениями":
        emoji = "🌥️"
    elif status == "ливневый дождь":
        emoji = "🌦️"
    elif status == "дождь":
        emoji = "🌧️"
    elif status == "гроза":
        emoji = "⛈️"
    elif status == "снег":
        emoji = "❄️"
    elif status == "туман" or status == "лёгкий туман":
        emoji = "🌫️"
    else:
        emoji = "❓"
    return emoji


def set_wind_emoji(wind):
    wind_emoji = ""
    if wind < 1.0:
        wind_emoji = "🍃"
    elif wind < 5.0:
        wind_emoji = "🌬️"
    elif wind < 10.0:
        wind_emoji = "💨"
    else:
        wind_emoji = "🌪️"
    return wind_emoji


def set_emoji_temperature(temperature):
    temperature_emoji = ""
    if temperature <= 0:
        temperature_emoji = "🥶"
    elif temperature <= 10:
        temperature_emoji = "❄️"
    elif temperature <= 20:
        temperature_emoji = "🌥️"
    elif temperature <= 30:
        temperature_emoji = "🌤️"
    else:
        temperature_emoji = "🥵"

    return temperature_emoji


def set_emoji_humidity(humidity):
    humidity_emoji = ""
    if humidity < 20:
        humidity_emoji = "🌵"
    elif humidity < 40:
        humidity_emoji = "🌾"
    elif humidity < 60:
        humidity_emoji = "🌿"
    elif humidity < 80:
        humidity_emoji = "💧"
    else:
        humidity_emoji = "🌧️"

    return humidity_emoji
