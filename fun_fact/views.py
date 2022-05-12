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

from fun_fact.models import FactDate
from fun_fact.numbersapi import URL_NUM_API, NumbersApiConnector
from fun_fact.serializers import FactDateSerializer, FactDateCreateSerializer, FactDateListSerializer, \
    FactDatePopularitySerializer


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


class FactDateCreateListDestroy(ModelCustomViewSet):
    serializer_class = FactDateSerializer
    queryset = FactDate.objects.all()
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return FactDateCreateSerializer
        elif self.action == 'list':
            return FactDateListSerializer
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
        # print(response)
        # print(response.content)
        # print(response.headers)
        print('to jest validated data', serializer.validated_data)
        numbers_api = NumbersApiConnector(serializer.validated_data)
        serializer.validated_data['fact'] = numbers_api.get_fact()
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
            return Response(
                {
                    "Failure": "Error",
                    "Error_list": {"Authorized Error": "please add header to your delete action X-API-KEY"}
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class PopularDateListAPIView(ListAPIView):
    serializer_class = FactDatePopularitySerializer

    def get_queryset(self):
        qs = FactDate.objects.values('month').annotate(days_checked=Count('id')).order_by('-days_checked', '-month')
        for i in range(len(qs)):
            qs[i].update({"id": len(qs) - i})
        return qs
