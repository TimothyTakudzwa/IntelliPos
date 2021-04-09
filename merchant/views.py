import logging

from django.conf import settings
from django.db import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
from .permissions import IsMerchantAdminUser, IsOwner


logger = logging.getLogger('gunicorn.error')


class MerchantProfileViewSet(viewsets.ModelViewSet):
    """
    Merchant Profile ViewSet
    """
    permission_classes = [IsAuthenticated, IsMerchantAdminUser, IsOwner]
    serializer_class = MerchantProfileSerializer
    queryset = MerchantProfile.objects.all()


class OperatorProfileViewSet(viewsets.ModelViewSet):
    """
    Operator Profile ViewSet
    """
    permission_classes = [IsAuthenticated, IsMerchantAdminUser, IsOwner]
    serializer_class = OperatorProfileSerializer
    queryset = OperatorProfile.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the operators
        for the currently authenticated merchant admin user.
        """
        user = self.request.user
        return self.queryset.filter(merchant=user.merchant_profile)


class POSTerminalViewSet(viewsets.ModelViewSet):
    """
    POS Terminal ViewSet
    """
    queryset = POSTerminal.objects.all()
    permission_classes = [IsAuthenticated, IsMerchantAdminUser, IsOwner]
    serializer_class = POSTerminalSerializer

    def get_queryset(self):
        """
        This view should return a list of all the terminals
        for the currently authenticated merchant admin user.
        """
        user = self.request.user
        return self.queryset.filter(merchant=user.merchant_profile)


    @action(detail=True, methods=['post'])
    def assign_operator(self, request, *args, **kwargs):
        """Assigns Operator to a POS Terminal"""
        pos = self.get_object()
        pos.operator = request.data['operator_id']
        pos.save()
        message = 'Assigned Operator'
        data = {
            'message': message,
       }
        logger.info(message)
        return Response(data)

    
    @action(detail=True, methods=['post'])
    def unassign_operator(self, request, *args, **kwargs):
        """Unassigns Operator from a POS Terminal"""
        pos = self.get_object()
        pos.operator = None
        pos.save()
        message = 'Unassigned Operator'
        data = {
            'message': message,
        }
        logger.info(message)
        return Response(data)