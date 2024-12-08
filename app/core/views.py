from django.db import transaction
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from app.core.models import Company, Document, Signer
from app.core.serializers import (
    CompanySerializer,
    DocumentSerializer,
    SignerSerializer,
)
from app.core.services import DocumentService
from typing import Any


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class SignerViewSet(ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerSerializer


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.document_service = DocumentService()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            with transaction.atomic():
                serializer = self.document_service.create_document(request.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(
                {'error': f'Erro interno ao criar documento, {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
