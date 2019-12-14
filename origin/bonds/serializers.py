from rest_framework import serializers
from .models import Bond


class BondSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bond
        fields = ['id', 'isin', 'size', 'currency', 'maturity', 'lei']
