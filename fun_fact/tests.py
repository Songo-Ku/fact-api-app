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
        cls.FactDates_url_list = reverse("fun_fact:fact_dates-list")
        cls.FactDates_obj_1 = FactDatesFactory()
        super().setUpClass()

    def setUp(self):
        self.FactDates_amount_obj = FactDate.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_FactDates_status_201(self, mock):
        mock.return_value = 'zemsta faraona mocked value'
        valid_fact_dates = {"month": 1, "day": 31}
        response = self.client.post(self.FactDates_url_list, data=valid_fact_dates)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_FactDates_save_in_db(self, mock):
        mock.return_value = 'zemsta faraona mocked value'
        valid_fact_dates = {"month": 1, "day": 31}
        response = self.client.post(self.FactDates_url_list, data=valid_fact_dates)
        self.assertEquals(FactDate.objects.count(), self.FactDates_amount_obj + 1)

    def test_post_incorrect_date_status_400(self):
        response = self.client.post(self.FactDates_url_list, data={"month": 13, "day": 32})
        print(response.content_params)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)




