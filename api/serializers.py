from rest_framework import serializers

from merchant.models import User, Transaction


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'company_id', 'email']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['date', 'sender_account', 'destination_bank', 'receiver_account', 'currency', 'amount', 'reference',
                  'status']
