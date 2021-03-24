import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from .two_factor_auth import OTP

logger = logging.getLogger('gunicorn.error')


class AccountVerification(APIView):
    """View to verify user account"""
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        phone = kwargs['phone']
        otp = OTP(phone).generate()
        data = {'otp':otp}
        return Response(data)
 

    def post(self, request, *args, **kwargs):
        """"Verify if otp is correct, incorrect or expired"""
        phone = kwargs['phone']
        otp = request.data['otp']
        result = OTP(phone).verify(otp)

        if isinstance(result, bool) and result:
            return Response({'message':'Correct OTP'})

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
