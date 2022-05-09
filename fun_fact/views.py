import requests
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fun_fact.models import Dates
from fun_fact.numbersapi import URL_NUM_API
from fun_fact.serializers import DatesSerializer, DatesCreateSerializer, DatesListSerializer


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


class ListViewset(mixins.ListModelMixin, GenericViewSet):
    pass


class PopularViewSet(ListViewset):
    serializer_class = DatesSerializer
    queryset = Dates.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
