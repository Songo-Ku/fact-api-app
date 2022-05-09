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

    def validate_month(self, value):
        print('validuje month')
        print(value)
        MONTHS_DICT = {
            "1": "January"
        }
        if MONTHS_DICT.get(str(value)):
            return MONTHS_DICT.get(str(value))
        else:
            raise serializers.ValidationError("Please select month from range 1-12")
        return value


class PopularListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dates
        fields = ['month', 'day', 'days_checked']
        read_only_fields = ['pk', 'fact']