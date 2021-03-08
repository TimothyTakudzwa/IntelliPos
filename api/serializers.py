from merchant.models import User, Transaction
from rest_framework import serializers


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['date', 'sender_account', 'destination_bank','receiver_account', 'currency', 'amount', 'reference', 'status' ]
