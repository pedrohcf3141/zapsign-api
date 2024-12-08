import pytest
from model_bakery import baker
from app.core.models import Company, Document, Signer
from rest_framework.test import APIClient
from unittest.mock import patch
from django.conf import settings
from app.core.services import DocumentService
import responses



@pytest.fixture
def company():
    return baker.make(Company, api_token='fake_api_token')


@pytest.fixture
def document(company):
    return baker.make(Document, company=company)


@pytest.fixture
def signer(document):
    return baker.make(Signer, document=document)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def zapsign_client_mock(responses):
    url = f'{settings.ZAPSIGN_API_URL}/api/v1/docs'
    response_data = {
        'open_id': 999,
        'token': 'fake_document_token',
        'name': 'Test Document',
        'status': 'created',
        'created_at': '2024-01-01T00:00:00Z',
        'last_update_at': '2024-01-01T00:00:00Z',
        'signers': [
            {
                'token': 'fake_signer_token',
                'status': 'pending',
                'name': 'Test Signer',
                'email': 'signer@example.com',
            }
        ],
    }
    responses.add(
        responses.POST,
        url,
        status=200,
        json=response_data,
    )

    return responses


@pytest.fixture
def document_service_mock():
    with patch(DocumentService) as mock:
        instance = mock.return_value
        yield instance


@pytest.fixture
def zap_sign_client_mock():
    return
