from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from merchant.models import *
from user_auth.serializers import UserDetailsSerializer


class MerchantProfileSerializer(serializers.ModelSerializer):
    country = CountryField()
    phone_number = PhoneNumberField()
    class Meta:
        model = MerchantProfile
        fields = ('name', 'country', 'phone_number','address')

    def create(self, validated_data):
        user = self.context.get("request").user
        return MerchantProfile.objects.create(user=user, **validated_data)


class OperatorProfileSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    user =  UserDetailsSerializer()
    
    class Meta:
        model = OperatorProfile
        fields = ('first_name', 'last_name', 'phone_number', 'user')
      
    def create(self, validated_data):
        merchant_id = self.context.get("request").query_params.get('merchant_id')
        merchant = MerchantProfile.objects.get(pk=merchant_id)
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data, password='')
        return OperatorProfile.objects.create(
            user=user, 
            merchant = merchant,
            **validated_data
        )


class POSTerminalSerializer(serializers.ModelSerializer):
    operator = OperatorProfileSerializer(read_only=True)
    class Meta:
        model = POSTerminal
        fields = ('operator')
        read_only_fields = fields

    def create(self, validated_data):
        merchant_id = self.context.get("request").query_params.get('merchant_id')
        merchant = MerchantProfile.objects.get(pk=merchant_id)
        return POSTerminal.objects.create(merchant=merchant, **validated_data)
  