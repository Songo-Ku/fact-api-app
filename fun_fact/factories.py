import factory
import factory.fuzzy

from fun_fact import models


class FactDatesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FactDate

    fact = factory.Sequence(lambda n: 'Some text faked to test field fact %s' % n)
    day = factory.fuzzy.FuzzyChoice(list(range(1, 32)))
    month = factory.fuzzy.FuzzyChoice(list(range(1, 13)))
