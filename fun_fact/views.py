import requests

from django.db.models.aggregates import Sum
from django.db.models import Count, F, Value
from django.db.models.expressions import Window
from django.db.models.functions.window import Rank
from django.db.models.functions import RowNumber

from rest_framework import viewsets, permissions, status, mixins
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fun_fact.models import Dates
from fun_fact.numbersapi import URL_NUM_API
from fun_fact.serializers import DatesSerializer, DatesCreateSerializer, DatesListSerializer, DatesPopularitySerializer


class ModelCustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """
    A Customviewset that provides default `create()`, `destroy()` and `list()` actions.
    """
    pass


class DatesCreateListDestroy(ModelCustomViewSet):
    serializer_class = DatesSerializer
    queryset = Dates.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return DatesCreateSerializer
        elif self.action == 'list':
            return DatesListSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        print('jestem w create')
        print(request.data.get("month"))
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print(serializer.validated_data['month'])
        MONTHS_DICT = {
            'January': 1, 'February': 2, 'March': 3,
            'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9,
            'October': 10, 'November': 11, 'December': 12
        }
        url = URL_NUM_API.format(
            MONTHS_DICT.get(serializer.validated_data['month']),
            serializer.validated_data['day']
        )
        # print(url)
        response = requests.get(url)
        print(response)
        print(response.content)
        print(response.headers)

        serializer.validated_data['fact'] = response.content.decode("utf-8")
        # response.json()  # < do sprawdzenia
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        print(request)
        print(request.headers)
        instance = self.get_object()
        print(instance)
        if request.headers.get("X-API-KEY") == "SECRET_API_KEY":
            print('jest autoryzacja')
            print(request.headers.get("X-API-KEY"))
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            print('nie ma autoryzacji')
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PopularDateListAPIView(ListAPIView):
    serializer_class = DatesPopularitySerializer

    def get_queryset(self):
        qs = Dates.objects.values('month').annotate(days_checked=Count('id')).order_by('-days_checked', '-month')
        for i in range(len(qs)):
            qs[i].update({"id": len(qs) - i})
        return qs