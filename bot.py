import telebot
from weather import weather_info_api
from search_image import s_image
import TOKENS
from translator import translate_text_to_text, languages_list
import pytesseract
from PIL import Image, ImageEnhance
import io
import requests


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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


TRANSLATE_STATE_LANG_FROM = 3
TRANSLATE_STATE_LANG_TO = 4
TRANSLATE_STATE_TEXT = 5
OCR_STATE = 6
translate_data = {}


@bot.message_handler(commands=['translate'])
def handle_translate_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = TRANSLATE_STATE_LANG_FROM
    bot.send_message(
        chat_id, "С какого языка перевести? (Введите /languages для списка доступных языков)")


@bot.message_handler(commands=['languages'])
def send_languages(message):
    chat_id = message.chat.id
    languages = languages_list
    bot.send_message(chat_id, languages)


@bot.message_handler(commands=['ocr'])
def handle_ocr_command(message):
    chat_id = message.chat.id
    user_states[chat_id] = OCR_STATE
    bot.send_message(
        chat_id, "Отправьте изображение для распознавания текста.")


@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def handle_all_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, None)

    if state == WEATHER_STATE:
        city = message.text
        weather_info = weather_info_api(city)
        bot.send_message(chat_id, weather_info)
        del user_states[chat_id]
    elif state == SEARCH_IMAGE_STATE:
        query = message.text
        image_url = s_image(query)

        if image_url:
            bot.send_photo(chat_id, image_url)
        else:
            bot.send_message(chat_id, "Извините, ничего не найдено.")

        del user_states[chat_id]
    elif state == TRANSLATE_STATE_LANG_FROM:
        if message.text.lower() == '/languages':
            send_languages(message)
            return
        lang_from = message.text
        translate_data[chat_id] = {'lang_from': lang_from}
        user_states[chat_id] = TRANSLATE_STATE_LANG_TO
        bot.send_message(
            chat_id, "На какой язык перевести? (Введите /languages для списка доступных языков)")
    elif state == TRANSLATE_STATE_LANG_TO:
        if message.text.lower() == '/languages':
            send_languages(message)
            return
        lang_to = message.text
        translate_data[chat_id]['lang_to'] = lang_to
        user_states[chat_id] = TRANSLATE_STATE_TEXT
        bot.send_message(chat_id, "Введите текст для перевода:")
    elif state == TRANSLATE_STATE_TEXT:
        text_to_translate = message.text
        lang_from = translate_data[chat_id]['lang_from']
        lang_to = translate_data[chat_id]['lang_to']
        translated_text = translate_text_to_text(
            lang_from, lang_to, text_to_translate)  # Функция перевода
        bot.send_message(chat_id, translated_text)
        del user_states[chat_id]
        del translate_data[chat_id]
    elif state == OCR_STATE:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            file_path = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
            image_stream = requests.get(file_path).content
            image = Image.open(io.BytesIO(image_stream))
            enhancer = ImageEnhance.Contrast(image)
            image_enhanced = enhancer.enhance(2.0)
            # OCR процесс
            ocr_result = pytesseract.image_to_string(
                image_enhanced, lang='rus')

            if ocr_result.strip():
                bot.send_message(chat_id, ocr_result)
            else:
                bot.send_message(chat_id, "Не удалось распознать текст.")

            del user_states[chat_id]

        else:
            bot.send_message(
                chat_id, "Пожалуйста, отправьте фотографию для распознавания.")
    else:
        bot.send_message(
            chat_id, "Это не команда. Попробуйте /weather для получения погоды или /translate для перевода текста.")


print('Бот запущен')
bot.infinity_polling()
