import logging
import merchant
from django.db.models import Q

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

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import *
from .serializers import *
from .permissions import IsMerchantAdminUser, IsOwner
from intelli_sms_gateway.client import Client


logger = logging.getLogger('gunicorn.error')

client = Client('mgunityrone@gmail.com', '123abc!!!')

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


class TransactionsView(APIView):
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
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionUserView(APIView):
    serializer_class = DummyTransactionSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:

            user = self.request.user
            merchant = user.merchant_profile

            queryset = OperatorProfile.objects.all()
            print(user.id)
            operator = queryset.filter(merchant=user.merchant_profile, user=user.id).first()

            print("opetator", operator.pk)
            merchant_id = {
                "merchant_id": merchant.id,
                "user_id": user.id,
                "pk": operator.pk
            }
            return Response(merchant_id)
        except Exception as e:
            """
            EXCEPTION
            """
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetTransactionsView(APIView):
    serializer_class = DummyTransactionSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get(self, request, search):
        try:

            user = request.user
            user_merchant = MerchantProfile.objects.filter(user=user.id).first()
            
            lookups= Q(reference__icontains=search) | Q(status__icontains=search) | Q(selected_card__icontains=search)
            
            transaction = DummyTransaction.objects.filter(lookups, merchant=user_merchant).distinct()
            # transaction = DummyTransaction.objects.filter(merchant=user_merchant)
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
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EmailTransactionsView(APIView):
    serializer_class = DummyTransactionSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get(self, request, reference):
        try:

            user = request.user
            user_merchant = MerchantProfile.objects.filter(user=user.id).first()
            
            transaction = DummyTransaction.objects.filter(reference=reference, merchant=user_merchant).first()
            # transaction = DummyTransaction.objects.filter(merchant=user_merchant)
            serializer = DummyTransactionSerializer(transaction, many=True)
            if serializer.is_valid:
                import smtplib, ssl

                port = 465  # For SSL
                smtp_server = "smtp.gmail.com"
                sender_email = "zulunigelbintelliposlive@gmail.com"  # Enter your address
                # zulunigelbintelliposlive
                receiver_email = user.email  # Enter receiver address
                password = "jikatino"

                message = MIMEMultipart("alternative")
                message["Subject"] = f"Receipt With Rerefere: {reference}"
                message["From"] = sender_email
                message["To"] = receiver_email

                # Create the plain-text and HTML version of your message
               
                html = """\
                <html>
                <body>
                    <p>Good day,<br>
                    <b>Your transaction details<b/><br>
                    Reference Number: """ + reference + """<br></br>
                    Amount: """ + str(transaction.amount) + """<br></br>
                    Card Used: """ + transaction.selected_card + """<br></br>
                    Status: """ + transaction.status + """<br></br>
                    Date: """ + str(transaction.date) + """<br></br>

                    </p>
                </body>
                </html>
                """

                # Turn these into plain/html MIMEText objects
                part2 = MIMEText(html, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                message.attach(part2)

                # Create secure connection with server and send email
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, message.as_string()
                    )


                message = f"Good day, Your transaction details. Reference Number: {reference}. Amount: {str(transaction.amount)} Card Used: {transaction.selected_card } Status: {transaction.status} Date: {str(transaction.date)}"
                phone = str(user_merchant.phone_number)
                phone_number = phone.replace("+", "")
                client.send_single_sms(message, phone_number, 'IntelliPos')

                return JsonResponse(status=status.HTTP_200_OK, data={"message": "email sent"})
            else:
                """
                SERIALIZER ERRORS
                """
                return JsonResponse(status=status.HTTP_406_NOT_ACCEPTABLE, data={"errors": serializer.errors})
        except Exception as e:
            """
            EXCEPTION
            """
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
