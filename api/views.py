from django.http import Http404
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from merchant.models import Transaction
from merchant.models import User, IntelliPos
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
