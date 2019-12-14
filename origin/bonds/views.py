from rest_framework import viewsets

from .models import Bond
from .serializers import BondSerializer


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def get_queryset(self):
        user = self.request.user
        return Bond.objects.filter(author=user)

    def create(self, request):
        request.data.author = request.user
        return super().create(request)
