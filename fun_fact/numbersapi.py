import requests
import socket

from rest_framework.exceptions import APIException

URL_NUM_API = 'http://numbersapi.com/{}/{}/date'
MONTHS_DICT = {
    'January': 1, 'February': 2, 'March': 3,
    'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9,
    'October': 10, 'November': 11, 'December': 12
}


class NumbersApiConnectorError(APIException):
    pass


class NumbersApiConnector:
    def __init__(self, data):
        self.month = data.get("month")
        self.day = data.get("day")

    def get_response(self):
        try:
            url = URL_NUM_API.format(
                MONTHS_DICT.get(self.month),
                self.day
            )
            response = requests.get(url)
        except socket.error as e:
            raise NumbersApiConnectorError(e)
        return response

    def get_fact(self):
        response = self.get_response()
        return response.content.decode('UTF-8')
