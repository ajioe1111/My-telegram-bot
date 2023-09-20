import requests
title = input("Enter movie title: ")
data = requests.get('http://www.omdbapi.com/?t={title}&apikey=cc9e08d9')
result = data.json()
print(result)
