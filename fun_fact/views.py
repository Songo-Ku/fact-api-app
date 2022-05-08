import requests
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from fun_fact.models import Dates
from fun_fact.numbersapi import URL_NUM_API
from fun_fact.serializers import DatesSerializer, DatesCreateSerializer, DatesListSerializer


class DatesViewSets(viewsets.ModelViewSet):
    serializer_class = DatesSerializer
    queryset = Dates.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = []

    def get_serializer_class(self):
        if self.action == 'create':
            return DatesCreateSerializer
        elif self.action == 'list':
            return DatesListSerializer
        # elif self.action == 'update':
        #     return OrderedProductsUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'destroy':
            # permission_classes = [permissions.IsAuthenticated]
            permission_classes = []
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

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
        serializer.validated_data['fact'] = response.content.decode("utf-8")
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









