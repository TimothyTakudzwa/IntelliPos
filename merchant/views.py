import logging

from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

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
    serializer_class = OperatorProfileSerializer
    queryset = OperatorProfile.objects.all()


class POSTerminalViewSet(viewsets.ModelViewSet):
    """
    POS Terminal ViewSet
    """
    permission_classes = [IsAuthenticated, IsMerchantAdminUser]
    serializer_class = POSTerminalSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = POSTerminal.objects.all()
        merchant_id = self.request.query_params.get('merchant_id')
        if merchant_id is not None:
            queryset = queryset.filter(merchant__pk=merchant_id)
        return queryset


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
 












