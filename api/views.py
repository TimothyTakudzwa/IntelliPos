from django.shortcuts import render
from merchant.models import Transaction
from .serializers import UserSerializer, TransactionSerializer
from rest_framework import viewsets
from merchant.models import User

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    Merchant User ViewSet
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    Merchant User ViewSet
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer