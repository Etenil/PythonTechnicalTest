from rest_framework import serializers
from .models import Bond, LegalEntity
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]


class BondSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(many=False, read_only=False)
    legal_name = serializers.StringRelatedField(many=False, read_only=False)

    class Meta:
        model = Bond
        fields = [
            'id',
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name',
            'author'
        ]

    def is_valid(self, raise_exception=False):
        validity = super().is_valid(raise_exception)

        # Reinjecting author and legal_name here. The validation somehow
        # strips them despite being some of the declared fields.
        self._validated_data['author'] = self.initial_data['author']
        self._validated_data['legal_name'] = self.initial_data['legal_name']
        return validity


class LegalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = ['name']
