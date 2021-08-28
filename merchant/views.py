import logging
import merchant

from django.conf import settings
from django.db import IntegrityError
import json
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
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


class PostTransactionsView(APIView):
    serializer_class = DummyTransactionSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:

            data = request.body
            user = request.user
            payload = json.loads(data)
            serializer = DummyTransactionSerializer(data=request.data)

            user_merchant = MerchantProfile.objects.filter(user=user.id).first()

            if serializer.is_valid():

                transaction = DummyTransaction.objects.create(
                    amount=payload["amount"],
                    reference=payload["reference"],
                    status=payload["status"],
                    selected_card=payload["selected_card"],
                    merchant=user_merchant,
                )
                transaction.save()
                return JsonResponse(status=status.HTTP_200_OK, data={"message": "transaction added successfully"})
            else:
                """
                SERIALIZER ERRORS
                """
                return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data={"errors": serializer.errors})
        except Exception as e:
            """
            EXCEPTION
            """
            return JsonResponse(data={'error': e}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:

            user = request.user
            user_merchant = MerchantProfile.objects.filter(user=user.id).first()
            
            transaction = DummyTransaction.objects.filter(merchant=user_merchant)
            serializer = DummyTransactionSerializer(transaction, many=True)
            if serializer.is_valid:
                return Response(serializer.data)
            else:
                """
                SERIALIZER ERRORS
                """
                return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data={"errors": serializer.errors})
        except Exception as e:
            """
            EXCEPTION
            """
            return JsonResponse(data={'error': e}, status=status.HTTP_400_BAD_REQUEST)
