import pytest


@pytest.mark.django_db
def test_company_str_method(company):
    assert str(company) == company.name


@pytest.mark.django_db
def test_document_str_method(document):
    assert str(document) == document.name


@pytest.mark.django_db
def test_signer_str_method(signer):
    assert str(signer) == signer.name
