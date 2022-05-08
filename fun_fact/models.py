from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# Create your models here.

MONTHS_CHOICES = (
    ('January', 1),
    ('February', 2),
    ('March', 3),
    ('April', 4),
    ('May', 5),
    ('June', 6),
    ('July', 7),
    ('August', 8),
    ('September', 9),
    ('October', 10),
    ('November', 11),
    ('December', 12),
)


class Dates(models.Model):
    MONTHS_CHOICES = (
        ('January', 1),
        ('February', 2),
        ('March', 3),
        ('April', 4),
        ('May', 5),
        ('June', 6),
        ('July', 7),
        ('August', 8),
        ('September', 9),
        ('October', 10),
        ('November', 11),
        ('December', 12),
    )
    month = models.CharField(choices=MONTHS_CHOICES, max_length=60, validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])
    day = models.IntegerField(
        validators=[
            MaxValueValidator(31),
            MinValueValidator(1)
        ]
    )
    fact = models.CharField(max_length=300)


class Month(models.Model):
    month = models.CharField(choices=MONTHS_CHOICES, max_length=60, unique=True)
    days_checked = models.IntegerField()