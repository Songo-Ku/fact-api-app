import socket

from rest_framework import serializers
import datetime

from fun_fact.models import FactDate
from fun_fact.numbersapi import MONTHS_DICT

MONTHS_NUMBER_DICT = {
    "1": "January",
    "2": "February",
    "3": "March",
    "4": "April",
    "5": "May",
    "6": "June",
    "7": "July",
    "8": "August",
    "9": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


class FactDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactDate
        fields = ['id', 'month', 'day']
        read_only_fields = ['id']


class FactDateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactDate
        fields = ['id', 'month', 'day', 'fact']
        read_only_fields = ['id']


class FactDateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactDate
        fields = ['id', 'month', 'day', 'fact']
        read_only_fields = ['id', 'fact']

    def validate_month(self, value):
        # print('validuje month')
        # print(value)
        if MONTHS_NUMBER_DICT.get(str(value)):
            return MONTHS_NUMBER_DICT.get(str(value))
        else:
            raise serializers.ValidationError("Please select month from range 1-12")

    def validate(self, data):
        if MONTHS_DICT.get(data.get('month')):
            month_ = MONTHS_DICT.get(data.get('month'))
        else:
            raise serializers.ValidationError("Please select month from range 1-12")
        day_ = int(data.get('day'))
        year_ = int(datetime.datetime.today().strftime("%Y"))
        try:
            datetime.datetime(year_, month_, day_)
        except:
            raise serializers.ValidationError("Inproperly selected day and month. That date doesnt exist!")
        return data


class FactDatePopularitySerializer(serializers.ModelSerializer):
    days_checked = serializers.ReadOnlyField()
    serializers.IntegerField()

    class Meta:
        model = FactDate
        fields = ['id', 'month', 'days_checked']