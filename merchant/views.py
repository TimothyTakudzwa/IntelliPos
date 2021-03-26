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
 












