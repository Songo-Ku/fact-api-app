from unittest.mock import Mock, patch


from django.db.models import Max
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from fun_fact.factories import FactDatesFactory
from fun_fact.models import FactDate


class FactDatesCreateListDestroyViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.FactDates_url_list = reverse("fun_fact:date-list")
        cls.FactDates_obj_1 = FactDatesFactory()
        super().setUpClass()

    def setUp(self):
        self.FactDates_amount_obj = FactDate.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_FactDates_status_201(self, mock):
        mock.return_value = 'Xyz'
        valid_FactDates = {"month": 1, "day": 31}
        response = self.client.post(self.FactDates_url_list, data=valid_FactDates)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_correct_post_FactDates_save_in_db(self):
        valid_FactDates = {"month": 1, "day": 31}
        response = self.client.post(self.FactDates_url_list, data=valid_FactDates)
        self.assertEquals(FactDate.objects.count(), self.FactDates_amount_obj + 1)



        # mockowanie
        # 1 1
        # JJanuary 1st is the day in 1994 that the Zapatista Army of National Liberation initiates twelve days of armed conflict in the Mexican State of Chiapas.
        # 5 5
        # May 5th is the day in 553 that the Second Council of Constantinople begins.