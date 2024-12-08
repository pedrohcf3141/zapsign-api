from django.db import transaction
from app.core.models import Company, Document, Signer
from app.core.serializers import DocumentSerializer
from app.core.external import ZapSignClient, ZapSignError
from typing import Dict, Any, List


class DocumentService:
    def __init__(self):
        self.zap_sign_client_class = ZapSignClient

    def create_document(self, document_data: Dict[str, Any]) -> DocumentSerializer:
        company = Company.objects.get(id=document_data.get('company'))
        zap_sign_client = self.zap_sign_client_class.get_instance(company.api_token)

        zap_sign_response = self._create_document_in_zapsign(document_data, zap_sign_client)
        zap_sign_data = zap_sign_response.json()

        document = self._save_document(zap_sign_data, document_data)
        self._create_signers(zap_sign_data.get('signers', []), document)

        return DocumentSerializer(document)

    def _create_document_in_zapsign(
        self,
        document_data: Dict[str, Any],
        zap_sign_client: ZapSignClient,
    ) -> Any:
        try:
            document_data['created_by'] = "" # Retirei os usuarios
            return zap_sign_client._session.post('/api/v1/docs', json=document_data)
        except ZapSignError as e:
            raise ValueError(f'Erro ao criar documento na ZapSign: {str(e)}')

    def _save_document(
        self,
        zap_sign_data: Dict[str, Any],
        original_data: Dict[str, Any],
    ) -> Document:
        document_data = {
            'open_id': zap_sign_data.get('open_id'),
            'token': zap_sign_data.get('token'),
            'name': zap_sign_data.get('name'),
            'status': zap_sign_data.get('status'),
            'created_at': zap_sign_data.get('created_at'),
            'last_updated_at': zap_sign_data.get('last_update_at'),
            'created_by': "", # Retirei os usuarios
            'company': original_data.get('company'),
        }
        serializer = DocumentSerializer(data=document_data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def _create_signers(self, signers_data: List[Dict[str, Any]], document: Document) -> None:
        try:
            with transaction.atomic():
                signers = [
                    Signer(
                        token=signer_data.get('token'),
                        status=signer_data.get('status'),
                        name=signer_data.get('name'),
                        email=signer_data.get('email'),
                        document=document,
                    )
                    for signer_data in signers_data
                ]
                Signer.objects.bulk_create(signers)
        except Exception as e:
            raise ValueError(f'Erro ao criar signatários: {str(e)}')
