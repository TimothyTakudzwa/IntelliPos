import datetime
import uuid

from django.db import models
from merchant.models import MerchantProfile

"""
    CATEGORY
"""

class Category(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False)
    image = models.FileField(blank=False, null=False, default='')
    description = models.CharField(max_length=30, blank=False)
    merchant = models.ForeignKey(MerchantProfile, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_children(self):
        return Product.objects.filter(category=self)    

    class Meta:
        ordering = ["last_updated"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False)
    brand = models.CharField(max_length=30, blank=False)
    price = models.FloatField()
    image = models.FileField(blank=False, null=False, default='')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    units = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    bar_code = models.CharField(max_length=255, default='')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["last_updated"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    @classmethod
    def get_shop_products(cls, merchant):
        return cls.objects.filter(category__merchant=merchant)

