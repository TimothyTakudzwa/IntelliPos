from rest_framework import serializers
from .models import User
from merchant.models import MerchantProfile


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        read_only_fields = ('email',)
        extra_kwargs = {'password': {'write_only': True}}
