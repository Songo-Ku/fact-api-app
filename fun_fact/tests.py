import json
from unittest.mock import Mock, patch

from django.db.models import Max
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from fun_fact.factories import FactDatesFactory
from fun_fact.models import FactDate
from fun_fact.serializers import FactDateListSerializer


class FactDatesCreateListDestroyViewSetTestCase(APITestCase):
    delete_date_fact_uri = '/dates/{}/'

    @classmethod
    def setUpClass(cls):
        cls.fact_dates_list_url = reverse("fun_fact:dates-list")
        cls.popular_list_url = reverse("fun_fact:popular-list")

        cls.fact_dates_1 = FactDatesFactory()
        super().setUpClass()

    def setUp(self):
        self.fact_dates_amount_obj = FactDate.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_FactDates_status_201(self, mock):
        mock.return_value = 'zemsta faraona mocked value'
        valid_fact_dates = {"month": 1, "day": 31}
        response = self.client.post(self.fact_dates_list_url, data=valid_fact_dates)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_create_correct_post_fact_dates_save_in_db(self, mock):
        mock.return_value = 'zemsta faraona mocked value'
        valid_fact_dates = {"month": 1, "day": 31}
        response = self.client.post(self.fact_dates_list_url, data=valid_fact_dates)
        self.assertEquals(FactDate.objects.count(), self.fact_dates_amount_obj + 1)

    def test_post_incorrect_date_fact_error_month_day(self):
        response = self.client.post(self.fact_dates_list_url, data={"month": 13, "day": 32})
        self.assertEquals(
            {
                'month': ['Please select month from range 1-12'],
                'day': ['Ensure this value is less than or equal to 31.']
            },
            json.loads(response.content)
        )

    def test_post_incorrect_date_status_400(self):
        response = self.client.post(self.fact_dates_list_url, data={"month": 13, "day": 32})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_incorrect_date_fact_validator_create_datetime_obj(self):
        response = self.client.post(self.fact_dates_list_url, data={"month": 2, "day": 31})
        self.assertEquals(
            {'non_field_errors': ['Inproperly selected day and month. That date doesnt '
                                  + 'exist!']},
            json.loads(response.content)
        )

    def test_list_dates_facts_200(self):
        response = self.client.get(self.fact_dates_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_obj_in_list(self):
        response = self.client.get(self.fact_dates_list_url)
        self.assertIn(FactDateListSerializer(self.fact_dates_1).data, json.loads(response.content.decode('utf-8')))

    def test_list_dates_facts_fetch_proper_amount_obj(self):
        response = self.client.get(self.fact_dates_list_url)
        self.assertEqual(FactDate.objects.count(), self.fact_dates_amount_obj)
        self.assertEqual(len(response.data), self.fact_dates_amount_obj)

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_delete_object_dates_204(self, mock):
        mock.return_value = 'fun text for object to delete'
        response = self.client.post(self.fact_dates_list_url, data={"month": 12, "day": 13})
        number_obj_before_delete = FactDate.objects.count()
        self.client.delete(
            reverse("fun_fact:dates-detail", kwargs={'pk': response.data.get("id")}),
            None,
            **{'HTTP_X-API-KEY': 'SECRET_API_KEY'}
        )
        self.assertEquals(FactDate.objects.count(), number_obj_before_delete - 1)

    @patch('fun_fact.numbersapi.NumbersApiConnector.get_fact')
    def test_delete_object_dates_401(self, mock):
        mock.return_value = 'fun text for object to delete'
        response = self.client.post(self.fact_dates_list_url, data={"month": 12, "day": 13})
        detele_url = f'/dates/{response.data.get("id")}/'
        response = self.client.delete(detele_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(self.fact_dates_amount_obj + 1, FactDate.objects.count())

    def test_delete_all_obj_fetch_empty_list(self):
        response = self.client.delete(
            reverse("fun_fact:dates-detail", kwargs={'pk': self.fact_dates_1.id}),
            None,
            **{"HTTP_X-API-KEY": "SECRET_API_KEY"}
        )
        response1 = self.client.get(self.fact_dates_list_url)
        self.assertEquals([], response1.data)

    def test_delete_not_extisting_obj(self):
        response = self.client.delete(
            reverse("fun_fact:dates-detail", kwargs={'pk': 1555}),
            None,
            **{"HTTP_X-API-KEY": "SECRET_API_KEY"}
            )
        self.assertEquals(404, response.status_code)
        self.assertEquals({"detail":"Not found."}, json.loads(response.content))


class PopularListViewSetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.fact_dates_list_url = reverse("fun_fact:dates-list")
        cls.popular_list_url = reverse("fun_fact:popular-list")
        cls.all_objects_dates_facts = FactDate.objects.all()
        cls.all_objects_dates_facts.delete()
        super().setUpClass()

    def setUp(self):
        self.fact_dates_amount_obj = FactDate.objects.filter().aggregate(max_id=Max('pk')).get('max_id')

    def test_delete_all_obj_fetch_empty_list(self):
        # self.fact_dates_1 = FactDatesFactory()
        response1 = self.client.get(self.popular_list_url)
        self.assertEquals([], response1.data)

    def test_pupular_ranking_one_obj(self):
        self.fact_dates_x1 = FactDatesFactory()
        response1 = self.client.get(self.popular_list_url)
        self.assertEquals(
            [{
                "id": 1,
                "month": str(self.fact_dates_x1.month),
                "days_checked": FactDate.objects.count()
            }],
            json.loads(response1.content)
        )

    def test_pupular_ranking_two_differ_months_objects_same_checked_days(self):
        self.fact_dates_x1 = FactDatesFactory(fact='cos tam', day=1, month=1)
        self.fact_dates_x2 = FactDatesFactory(fact='cos tam2', day=1, month=2)
        response1 = self.client.get(self.popular_list_url)
        self.assertEquals(
            [
                {
                    "id": 2,
                    "month": str(self.fact_dates_x2.month),
                    "days_checked": 1
                },
                {
                    "id": 1,
                    "month": str(self.fact_dates_x1.month),
                    "days_checked": 1
                }
            ],
            json.loads(response1.content)
        )

    def test_pupular_ranking_two_differ_months_not_equal_records(self):
        self.fact_dates_x1 = FactDatesFactory(fact='cos tam', day=1, month=1)
        self.fact_dates_x2 = FactDatesFactory(fact='cos tam2', day=1, month=1)
        self.fact_dates_x3 = FactDatesFactory(fact='cos tam3', day=1, month=2)
        response1 = self.client.get(self.popular_list_url)
        self.assertEquals(
            [
                {
                    "id": 2,
                    "month": str(self.fact_dates_x1.month),
                    "days_checked": 2
                },
                {
                    "id": 1,
                    "month": str(self.fact_dates_x3.month),
                    "days_checked": 1
                }
            ],
            json.loads(response1.content)
        )








