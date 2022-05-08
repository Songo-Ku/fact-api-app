from rest_framework import serializers

from fun_fact.models import Dates


class DatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = ['month', 'day']
        read_only_fields = ['pk']


class DatesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = ['month', 'day', 'fact']
        read_only_fields = ['pk']


class DatesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = ['month', 'day', 'fact']
        read_only_fields = ['pk', 'fact']

