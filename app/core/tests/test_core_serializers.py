import pytest
from app.core.models import Company, Document
from app.core.serializers import (
    CompanySerializer,
    DocumentSerializer,
    SignerSerializer,
)


@pytest.mark.django_db
def test_company_serializer():
    data = {
        'name': 'Test Company',
        'api_token': 'test_api_token_123',
    }
    serializer = CompanySerializer(data=data)
    assert serializer.is_valid()
    company = serializer.save()
    assert company.name == data['name']
    assert company.api_token == data['api_token']


@pytest.mark.django_db
def test_document_serializer():
    company = Company.objects.create(name='Test Company', api_token='token')
    data = {
        'open_id': 1,
        'token': 'doc_token_123',
        'name': 'Test Document',
        'status': 'created',
        'company': company.id,
    }
    serializer = DocumentSerializer(data=data)
    assert serializer.is_valid()
    document = serializer.save(created_by='Test User')
    assert document.name == data['name']
    assert document.status == data['status']
    assert document.company == company


@pytest.mark.django_db
def test_signer_serializer():
    document = Document.objects.create(
        open_id=1,
        token='doc_token_123',
        name='Test Document',
        status='created',
        created_by='Test User',
        company=Company.objects.create(name='Test Company', api_token='token'),
    )
    data = {
        'token': 'signer_token_123',
        'status': 'pending',
        'name': 'Test Signer',
        'email': 'test@signer.com',
        'document': document.id,
    }
    serializer = SignerSerializer(data=data)
    assert serializer.is_valid()
    signer = serializer.save()
    assert signer.name == data['name']
    assert signer.document == document
