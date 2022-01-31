import datetime
import uuid


from django.utils import timezone
from django.db import models
from merchant.models import POSTerminal

"""
    Transaction
"""


class Transctions(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=timezone.now)
    amount = models.FloatField(default=0.00, blank=True)
    reference = models.CharField(max_length=255, default='', unique=True)
    status = models.CharField(max_length=255, default='', blank=True)
    client = models.CharField(max_length=255, default='', blank=True) # client name eg Visa, Mastercard
    pos_terminal = models.ForeignKey(
        POSTerminal, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='transactions'
    )
    upstream_response = models.TextField()
    extras = models.JSONField(null=True, blank=True)
