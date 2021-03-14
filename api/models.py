from django.db import models


class JWTToken(models.Model):
    """
    Model Class for KMS Access and Refresh Token
    """
    name = models.TextField(max_length=30, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)

    @classmethod
    def get_access_token(cls, name):
        token = cls.objects.filter(name=name).first()
        return token.access_token

    @classmethod
    def get_refresh_token(cls, name):
        token = cls.objects.filter(name=name).first()
        return token.refresh_token

# Create your models here.
