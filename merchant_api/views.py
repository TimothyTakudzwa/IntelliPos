import random
import uuid
import datetime

from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from merchant.constants import create_account_email_user
from merchant.models import User, IntelliPos, Merchant, Transaction
from .helper_functions import *
from .models import JWTToken
from .serializers import TransactionSerializer
from django.conf import settings
from kms_client_api import KMSCLIENTAPI


# Create your views here.
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
    """
    Get DEK Viewset
    """

    def get(self, request):
        key_name = self.request.GET.get('key_name')        
        message = KMSCLIENTAPI().request_dek(key_name)               
        return JsonResponse(status=status, data={'message': message})


class ResetPassword(APIView):
    def get(self, request):
        email = self.request.POST.get('email')
        print(email)
        user = User.objects.filter(email=email).first()
        if user is not None:
            otp = random.randint(0, 99999)
            user.otp = str(otp)
            message = "A password reset was initiated for your account. Please Enter the OTP " + str(
                otp) + " on the mobile app to reset"
            user.save()
            send_mail(
                'IntelliPOS Password Reset',
                message,
                'timothytakudzwa@gmail.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse(status=200, data={'success': True, 'message': "OTP Sent"})
        else:
            return JsonResponse(status=200, data={'success': False, 'message': "Invalid Email"})

    def post(self, request):
        data = self.request.POST.get('data')
        email = self.request.POST.get('email')
        action = self.request.POST.get('action')
        user = User.objects.filter(email=email).first()
        if user is not None:
            if action == 'verify_otp':
                if data == user.otp:
                    success = True
                    message = 'OTP Match'
                else:
                    success = False
                    message = 'OTP Mismatch'
            else:
                if not password_used(user, data.encode('utf8')):
                    user.password = bcrypt.hashpw(data.encode('utf8'), bcrypt.gensalt()).decode()
                    user.password_change = datetime.datetime.now() + datetime.timedelta(3 * 30)
                    user.save()
                    success = True
                    message = "Password Updated"
                else:
                    success = False
                    message = "You cannot repeat a password you have used before"
        else:
            success = False
            message = "User Does not Exist"
        return JsonResponse(status=200, data={'success': success, 'message': message})


class RegisterViewSet(APIView):
    """
    Register User ViewSet
    """

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_id = request.POST.get('company_id')
        email = request.POST.get('email_address')
        merchant = Merchant.objects.filter(id=int(company_id)).first()
        token = uuid.uuid4().hex[:100]
        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode()

        if username_exists:
            return JsonResponse(status=401, data={'detail': 'Username Exists'})
        if email_exists:
            return JsonResponse(status=401, data={'detail': 'Email Exists'})

        user = User(username=username, password=password, email=email, role='TELLER',
                    first_name=first_name, last_name=last_name, \
                    merchant=merchant)
        user.save()
        full_name = first_name + ' ' + last_name
        pos_id = uuid.uuid4().hex[:5]
        pos = IntelliPos(merchant=merchant, pos_id=pos_id)
        pos.save()

        send_mail(
            'IntelliPOS Merchant Account',
            create_account_email_user.format(full_name, merchant.name, 'TELLER', username, pos_id),
            'timothytakudzwa@gmail.com',
            [email],
            fail_silently=False,
        )
        return JsonResponse(status=200, data={'detail': 'User Created Succesfully'})


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
