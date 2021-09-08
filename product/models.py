import datetime
import uuid

from django.db import models

"""
    Product
"""

class Product(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False)
    brand = models.CharField(max_length=30, blank=False)
    price = models.FloatField()
    image = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    units = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["last_updated"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

