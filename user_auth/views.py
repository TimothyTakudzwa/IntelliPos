import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from dj_rest_auth import views

from .two_factor_auth import OTP
from .helper_functions import send_otp

logger = logging.getLogger('gunicorn.error')


class LoginView(views.LoginView):
    
    def get_response(self):
        response = super().get_response()
        if self.user.locked_out:
            data = {
                'error': {
                    'code':'005',
                    'message':f'Maximum logon attempts reached, try again in {settings.USER_LOCKOUT_DURATION} minutes'}
            }
            return Response(data, status.HTTP_403_FORBIDDEN)
        return response


class AccountVerification(APIView):
    """View to verify user account"""
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        phone = kwargs['phone']
        otp = OTP(phone).generate()
        send_otp(phone)
        return Response()
 

    def post(self, request, *args, **kwargs):
        """"Verify if otp is correct, incorrect or expired"""
        phone = kwargs['phone']
        otp = request.data['otp']
        result = OTP(phone).verify(otp)
        if isinstance(result, bool) and result:
            return Response()
        elif isinstance(result, bool) and not result:
            data = {
                'error': {
                    'code':'001',
                    'message':'Incorrect OTP'}
            }
            logger.info(data)
            return Response(data, status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                'otp': result,
                'error': {
                    'code': '002',
                    'message': 'Expired OTP'}
            }
            logger.info(data)
            return Response(data, status.HTTP_401_UNAUTHORIZED)
