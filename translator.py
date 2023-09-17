from googletrans import Translator


def translate_to_english(text):
    text_to_str = str(text)
    translator = Translator()
    result = translator.translate(text_to_str, dest='en')
    print(f'Translated text: {result.text} and original text: {text}')
    return result.text
