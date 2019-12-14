from datetime import date
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


CURRENCIES = [
    ('GBP', 'British Pound'),
    ('EUR', 'Euro'),
    ('USD', 'US Dollar')
]


class LegalEntity(models.Model):
    """
    This acts both as an easy way to query bonds per legal entity and also
    a form of cache for the remote API that feeds us LEI data, we can save
    time and reduce requests this way.
    """
    lei = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


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
    legal_name = models.ForeignKey(
        LegalEntity,
        on_delete=models.CASCADE,
        null=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
