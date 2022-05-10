from rest_framework import serializers

from fun_fact.models import Dates

MONTHS_DICT = {
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
        if MONTHS_DICT.get(str(value)):
            return MONTHS_DICT.get(str(value))
        else:
            raise serializers.ValidationError("Please select month from range 1-12")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        day = attrs.get('day')
        return attrs

    def xxxxdwdw(self):
        pass  #zrobic validayor ktory sprawdzi czy mozna zrobic date. cross field validation


class DatesPopularitySerializer(serializers.ModelSerializer):
    days_checked = serializers.ReadOnlyField()
    serializers.IntegerField()

    class Meta:
        model = Dates
        fields = ['id', 'month', 'days_checked']