import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.core.models import Company, Signer, Document


@pytest.mark.django_db
def test_company_list(company):
    client = APIClient()
    url = reverse('company-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['name'] == company.name


@pytest.mark.django_db
def test_create_company():
    client = APIClient()
    url = reverse('company-list')
    data = {'name': 'Test Company', 'api_token': 'Test Token'}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Company.objects.count() == 1
    assert response.data['name'] == 'Test Company'


@pytest.mark.django_db
def test_signer_list(signer):
    client = APIClient()
    url = reverse('signer-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['name'] == signer.name


@pytest.mark.django_db
def test_create_signer(document):
    client = APIClient()
    url = reverse('signer-list')
    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'document': document.id,
        'token': document.token,
        'status': 'new',
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Signer.objects.count() == 1
    assert response.data['name'] == 'John Doe'


@pytest.mark.django_db
def test_document_list(document):
    client = APIClient()
    url = reverse('document-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['name'] == document.name


@pytest.mark.django_db
def test_create_document2(company, zapsign_client_mock):
    client = APIClient()
    url = reverse('document-list')
    data = {
        'name': 'Test Document',
        'company': company.id,
        'signers': [{'name': 'Test Signer', 'email': 'test@test.com'}],
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Document.objects.count() == 1
    assert response.data['name'] == 'Test Document'
    assert response.data['signers'][0]['name'] == 'Test Signer'


@pytest.mark.django_db
def test_create_document_error():
    client = APIClient()
    url = reverse('document-list')
    data = {
        'name': 'Test Document',
        'company': 999,
        'signers': [{'name': 'Teste Signer', 'email': 'test@test.com'}],
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'error' in response.data
