import requests
from translator import translate_to_english
import TOKENS


def image(query):
    query = translate_to_english(query)
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": TOKENS.UNSPLASH_ACCESS_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if len(data["results"]) > 0:
        return data["results"][0]["urls"]["full"]
    else:
        return None
