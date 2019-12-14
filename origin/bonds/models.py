from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


CURRENCIES = [
    ('GBP', 'British Pound'),
    ('EUR', 'Euro'),
    ('USD', 'US Dollar')
]


class Bond(models.Model):
    # ISIN identifies a company, it's a 12 characters long string with a
    # specific validation (format + the last character is a checksum)
    isin = models.CharField(max_length=12)
    size = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    # Registering a bond that matured in the past doesn't seem sensible
    maturity = models.DateField(null=False,
                                validators=[MinValueValidator(date.today())])
    # LEIs are 20 characters long, see ISO 17442:2012
    lei = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
