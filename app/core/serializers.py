from rest_framework import serializers
from app.core.models import Company, Document, Signer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'created_at', 'last_updated_at', 'api_token']


class SignerSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Signer
        fields = ['id', 'token', 'status', 'name', 'email', 'document']


class DocumentSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    created_by = serializers.SerializerMethodField()
    signers = SignerSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'open_id',
            'token',
            'name',
            'status',
            'created_at',
            'last_updated_at',
            'created_by',
            'company',
            'signers',
        ]

    def get_created_by(self, obj):
        return str(obj.created_by)
