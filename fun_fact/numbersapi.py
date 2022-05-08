import requests


URL_NUM_API = 'http://numbersapi.com/{}/{}/date'
url = URL_NUM_API.format(5, 5)
response = requests.get(url)
response.content.decode("utf-8")