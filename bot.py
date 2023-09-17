import telebot
from weather import weather_info_api
from search_image import image
import TOKENS

API_TOKEN = TOKENS.API_TELEGRAM

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Чо те надо? падва!')


user_states = {}

WEATHER_STATE = 1


@bot.message_handler(commands=['weather'])
def handle_weather_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = WEATHER_STATE
    bot.send_message(chat_id, "В каком городе вы хотите узнать погоду?")


SEARCH_IMAGE_STATE = 2


@bot.message_handler(commands=['image_unsplash'])
def handle_search_image_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = SEARCH_IMAGE_STATE
    bot.send_message(chat_id, "Какое изображение вы хотите найти?")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_message(message):
    chat_id = message.chat.id
    # Используем метод get() для безопасного доступа к элементу словаря
    state = user_states.get(chat_id, None)

    if state == WEATHER_STATE:
        city = message.text
        weather_info = weather_info_api(city)  # Заглушка
        bot.send_message(chat_id, weather_info)
        del user_states[chat_id]  # Сбрасываем состояние пользователя
    elif state == SEARCH_IMAGE_STATE:
        query = message.text
        image_url = image(query)

        if image_url:
            bot.send_photo(chat_id, image_url)
        else:
            bot.send_message(chat_id, "Извините, ничего не найдено.")

        del user_states[chat_id]
    else:
        bot.send_message(
            chat_id, "Это не команда. Попробуйте /weather для получения погоды или /image_unsplash для поиска изображения.")


bot.infinity_polling()
