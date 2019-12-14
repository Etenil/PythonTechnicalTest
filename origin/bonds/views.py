from rest_framework import viewsets

from .models import Bond
from .serializers import BondSerializer


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
