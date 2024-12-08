from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    api_token = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Document(models.Model):
    open_id = models.IntegerField(null=False)
    token = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.name


class Signer(models.Model):
    token = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='signers')

    def __str__(self):
        return self.name
