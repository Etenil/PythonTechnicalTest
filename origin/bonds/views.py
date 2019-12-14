from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Bond
from .serializers import BondSerializer


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def get_queryset(self):
        user = self.request.user
        return Bond.objects.filter(author=user)

    def create(self, request):
        req_data = dict(request.data)
        req_data['author'] = request.user.id

        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
