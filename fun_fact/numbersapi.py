import requests

from rest_framework.exceptions import APIException

URL_NUM_API = 'http://numbersapi.com/{}/{}/date'


class NumbersApiConnectorError(APIException):
    pass


class NumbersApiConnector:
    def __int__(self, data):
        data.get


url = URL_NUM_API.format(5, 5)
response = requests.get(url)
response.content.decode("utf-8")