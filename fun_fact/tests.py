from unittest.mock import Mock, patch


from django.db.models import Max
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from fun_fact.factories import DatesFactory
from fun_fact.models import Dates


class DatesCreateListDestroyViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.dates_url_list = reverse("fun_fact:date-list")
        cls.dates_obj_1 = DatesFactory()
        super().setUpClass()

    def setUp(self):
        self.dates_amount_obj = Dates.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_dates_status_201(self, mock):
        mock.return_value = 'Xyz'
        valid_dates = {"month": 1, "day": 31}
        response = self.client.post(self.dates_url_list, data=valid_dates)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_correct_post_dates_save_in_db(self):
        valid_dates = {"month": 1, "day": 31}
        response = self.client.post(self.dates_url_list, data=valid_dates)
        self.assertEquals(Dates.objects.count(), self.dates_amount_obj + 1)



        # mockowanie
        # 1 1
        # JJanuary 1st is the day in 1994 that the Zapatista Army of National Liberation initiates twelve days of armed conflict in the Mexican State of Chiapas.
        # 5 5
        # May 5th is the day in 553 that the Second Council of Constantinople begins.