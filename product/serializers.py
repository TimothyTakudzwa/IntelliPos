from product.models import Product
from rest_framework import serializers

from product.models import *

class ProductSerializer(serializers.ModelSerializer):
    # date = serializers.DateField()
    name = serializers.CharField(required=True)
    brand = serializers.CharField(required=True)
    price = serializers.FloatField()
    image = serializers.CharField()
    description = serializers.CharField()
    code = serializers.CharField(required=True)
    units = serializers.IntegerField(required=True)
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'brand',
            'price',
            'image',
            'description',
            'code',
            'units',
        ]
        read_only_fields = fields

    def create(self, validated_data):
        return ProductSerializer(**validated_data)
  