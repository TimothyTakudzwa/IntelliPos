from django.shortcuts import render
from merchant.models import Transaction
from .serializers import UserSerializer, TransactionSerializer
from rest_framework import viewsets
from .helper_functions import get_access_token
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from merchant.models import User
from rest_framework.permissions import IsAuthenticated
import requests
import json


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    """
    Merchant User ViewSet
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionProcessing(APIView):
    """
    Process an IntelliPOS Transaction
    """

    def post(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = TransactionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(APIView):
    """
    Login to Merchant Application Viewset
    """
    def post(self, request):
        data = request.data



class TransactionViewSet(APIView):
    """
    Retrieve, update or delete a transaction instance.
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        # url = 'http://45.55.44.41:8003/api/v1/keys'
        # access_token = get_access_token('intellipos')
        # headers = {"Content-Type": "application/json", "Authorization": f"access_token {access_token}"}
        # r = requests.get(url, headers=headers)
        # print(r.json())

        transaction = self.get_object(id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = TransactionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
