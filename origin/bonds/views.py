from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Bond, LegalEntity
from .serializers import BondSerializer, LegalEntitySerializer


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def get_queryset(self):
        user = self.request.user
        return Bond.objects.filter(author=user)

    def create(self, request):
        try:
            req_data = request.data.dict()
        except AttributeError:
            # This only happens in unit tests, the force_authentication
            # method creates a dict() instead of a QueryDict. It's probably
            # a bug.
            req_data = request.data

        req_data['author'] = request.user

        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LegalEntityViewSet(viewsets.ModelViewSet):
    queryset = LegalEntity.objects.all()
    serializer_class = LegalEntitySerializer
