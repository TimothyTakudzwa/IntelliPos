from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from merchant.models import *


class MerchantProfileSerializer(serializers.ModelSerializer):
    country = CountryField()
    phone_number = PhoneNumberField()
    class Meta:
        model = MerchantProfile
        fields = ('name', 'country', 'phone_number','address'),

    def create(self, validated_data):
        user = self.context.get("request").user
        return MerchantProfile.objects.create(user=user, **validated_data)


class OperatorProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = OperatorProfile
        fields = ('first_name', 'last_name', 'phone_number'),

    def create(self, validated_data):
        pass


class POSTerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSTerminal
        fields = ('pos_id'),

    def create(self, validated_data):
        pass
  