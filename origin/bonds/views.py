from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Bond, LegalEntity
from .serializers import BondSerializer, LegalEntitySerializer

from .gleif import get_entity_name, InvalidLeiError, LeiRequestError


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
    http_method_names = ['get', 'post', 'options', 'head']

    def get_queryset(self):
        user = self.request.user

        legal_name = self.request.query_params.get('legal_name', None)
        if legal_name is not None:
            try:
                legal_entity = LegalEntity.objects.get(name=legal_name)
                return Bond.objects.filter(
                    legal_name=legal_entity,
                    author=user
                )
            except LegalEntity.DoesNotExist:
                pass

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

        try:
            legal_name = LegalEntity.objects.get(pk=req_data['lei'])
        except LegalEntity.DoesNotExist:
            try:
                name = get_entity_name(req_data['lei'])
                legal_name = LegalEntity.objects.create(
                    lei=req_data['lei'],
                    name=name
                )
                legal_name.save()
            except InvalidLeiError:
                return Response(
                    {'error': 'Invalid LEI number provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except LeiRequestError:
                return Response(
                    {'error': 'Error getting LEI number information'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        req_data['legal_name'] = legal_name

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
