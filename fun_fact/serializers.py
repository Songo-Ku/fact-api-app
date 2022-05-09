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



#
# deale app Yb maja badac temat w tym tyg bo wczesniej byli w ograniczonym skladzie przez majowke
#   dzial technologii i adopsow dostal ticket
#   olx dalej cisza, nie odpisuja na pingi mailowe
# pkp problem zmraid
#
# Api adform:
#     mamy problemy,

# z tego cpo potrzebujemy ostatnia operacja natomiast dosyc istotna, nie tworzy nam się operacja, która do tej pory robiła się automatycznie,
# czekamy na instrukcje od adform o ile znów czegoś nie zmienią.
# mozliwe jest ze zabrali nam dostep bo cos poszlo nie tak po stronie ich serwera gdyż otrzymywaliśmy błędy 500, gdy robilismy testowe requesty.

# Dokumentacja i przeplywy są rozpisane w projekcie na gitlab. Przystepuje do kodowania, wiec zrobimy z MP konsultacje w tej sprawie.