from rest_framework.views import APIView
from rest_framework.response import Response

from .two_factor_auth import OTP

class AccountVerification(APIView):
    """View to verify user account"""
    pass
 