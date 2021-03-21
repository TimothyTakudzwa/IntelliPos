from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from merchant.models import User, Transaction, MerchantProfile


class MerchantProfileSerializer(serializers.ModelSerializer):
    country = CountryField()
    phone_number = PhoneNumberField()
    class Meta:
        model = MerchantProfile
        fields = ('name', 'country', 'phone_number','address'),

    def create(self, validated_data):
        user = self.context.get("request").user
        return MerchantProfile.objects.create(user=user, **validated_data)



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'company_id', 'email']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['date', 'sender_account', 'destination_bank', 'receiver_account', 'currency', 'amount', 'reference',
                  'status']
