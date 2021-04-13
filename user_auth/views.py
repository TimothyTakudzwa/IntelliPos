import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.conf import settings
from dj_rest_auth import views
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.app_settings import create_token
from django.core.cache import cache
from django.utils import timezone


from .two_factor_auth import OTP
from .helper_functions import send_otp

logger = logging.getLogger('gunicorn.error')


class LoginView(views.LoginView):
    

    def get_response(self):
        if self.user.locked_out:
            data = {
                'error': {
                    'code':'005',
                    'message':f'Maximum logon attempts reached, try again in {cache.ttl(self.user)//60} minutes'}
            }
            logger.warn(data)
            return Response(data, status.HTTP_403_FORBIDDEN)

        serializer_class = self.get_response_serializer()

        access_token_expiration = None
        refresh_token_expiration = None
        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import api_settings as jwt_settings
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(settings, 'JWT_AUTH_RETURN_EXPIRATION', False)

            data = {
                'user': self.user,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token
            }

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(instance=data,
                                          context=self.get_serializer_context())
        else:
            serializer = serializer_class(instance=self.token,
                                          context=self.get_serializer_context())

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if getattr(settings, 'REST_USE_JWT', False):
            from dj_rest_auth.jwt_auth import set_jwt_cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)
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
