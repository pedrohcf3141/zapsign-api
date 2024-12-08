import pytest
from app.core.models import Signer

# from app.core.external import ZapSignError
# from app.core.serializers import DocumentSerializer
from app.core.services import DocumentService


@pytest.mark.django_db
def test_create_create_signers(document):
    document_service = DocumentService()
    signers_data = [
        {
            'token': 'signer_token',
            'status': 'pending',
            'name': 'Signer 1',
            'email': 'signer1@example.com',
        },
    ]
    document_service._create_signers(signers_data, document)

    assert Signer.objects.count() == 1
