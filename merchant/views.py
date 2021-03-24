import logging
import random
import uuid
import datetime

from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from allauth.account import app_settings as allauth_settings
from rest_framework import status, viewsets
from rest_framework.response import Response

from merchant.constants import create_account_email_user
from .crypto import NISTApprovedCryptoAlgo
from .helper_functions import *
from .models import *
from .serializers import *
from .kms_client_api import KMSCLIENTAPI

logger = logging.getLogger('gunicorn.error')


class MerchantProfileViewSet(viewsets.ModelViewSet):
    """
    Merchant Profile ViewSet
    """
    serializer_class = MerchantProfileSerializer
    queryset = MerchantProfile.objects.all()


    def get_permissions(self):
        permission_classes = list()
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OperatorProfileViewSet(viewsets.ModelViewSet):
    """
    Operator Profile ViewSet
    """
    serializer_class = POSTerminalSerializer
    queryset = POSTerminal.objects.all()


class POSTerminalViewSet(viewsets.ModelViewSet):
    """
    POS Terminal ViewSet
    """
    serializer_class = POSTerminalSerializer
    queryset = POSTerminal.objects.all()


    @action(detail=True, methods=['post'])
    def assign_operator(self, request, *args, **kwargs):
        """Assigns Operator to a POS Terminal"""
        pos = self.get_object()
        pos.operator = request.data['operator']
        pos.save()
        message = 'Assigned Operator'
        data = {
            'message': message,
       }
        logger.info(message)
        return Response(data)
 












