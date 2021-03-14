from django.http import Http404
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
import logging

from merchant.models import Transaction
from merchant.models import User, IntelliPos
from .models import JWTToken
from .serializers import UserSerializer, TransactionSerializer


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


class DEKViewSet(APIView):

    def get(self, request):
        key_name = self.request.GET.get('key_name')
        url = 'http://45.55.44.41:8003/api/v1/keys/dek?key_name=' + key_name
        token = JWTToken.objects.filter(name='intellipos').first()
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token.access_token}"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            access_token = data['message']
            message = f"{access_token.encode('ISO-8859-1')}"
            success = True
        else:
            url = 'http://45.55.44.41:8003/api/v1/refresh_token'
            refresh_token = JWTToken.get_refresh_token('intellipos')
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token.refresh_token}"}
            r = requests.get(url, headers=headers)
            data = r.json()
            if r.status_code == 200:
                token.access_token = data['access_token']
                token.save()

            message = 'Failed to get DEK'
            success = False
        return JsonResponse(status=200, data={'success':success, 'message':message})


class LoginViewSet(APIView):
    """
    Login to Merchant Application Viewset
    """

    def post(self, request):
        try:
            data = request.data
            username = data['username']
            password = data['password']
            pos_id = data['posID']
            device = data['device']
            # Authenticate
            authenticated, description = IntelliPos.authenticate(username, password.encode('utf8'), pos_id, device)
            if authenticated:
                return JsonResponse(status=200, data={'success': True, 'detail': description})
            else:
                return JsonResponse(status=200, data={'success': False, 'detail': description})
        except Exception as e:
            print(e)
            return JsonResponse(status=500, data={'details': 'Invalid Request'})


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
