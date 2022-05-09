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

    def post_correct_dates(self):
        print(reverse("fun_fact:date-list"))
        valid_dates = {
            "month": 1,
            "day": 31,
            "fact": 'some test fact to post correct dates'
        }
        return self.client.post(self.dates_url_list, data=valid_dates)

    def test_create_correct_post_dates_status_201(self):
        response = self.post_correct_dates()
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Dates.objects.count(), self.dates_amount_obj + 1)