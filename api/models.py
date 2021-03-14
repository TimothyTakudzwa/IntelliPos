from django.db import models


class JWTToken(models.Model):
    """
    Model Class for KMS Access and Refresh Token
    """
    name = models.TextField(max_length=30, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)

# Create your models here.
