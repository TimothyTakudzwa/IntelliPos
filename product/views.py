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
from intelli_sms_gateway.client import Client


logger = logging.getLogger('gunicorn.error')

class PostProductView(APIView):
    serializer_class = ProductSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        try:
            data = request.body
            payload = json.loads(data)

            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid():

                product = Product.objects.create(
                    name=payload["name"],
                    brand=payload["brand"],
                    price=payload["price"],
                    image=payload["image"],
                    units=payload["units"],
                    description=payload["description"],
                    code=payload["code"],
                )
                product.save()
                return JsonResponse(status=status.HTTP_200_OK, data={"message": "product added successfully"})
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

class SearchProductView(APIView):
    serializer_class = ProductSerializer
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def get(self, request, code):
        try:
            print(code)
            product = Product.objects.filter(code=code).first()
            if product:
                payload = {
                    "name":product.name,
                    "brand": product.brand,
                    "price": product.price,
                    "image": product.image,
                    "units": product.units,
                    "description": product.description,
                    "code": product.code,
                }
                return Response(payload)
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={"message": "product not found"})
        except Exception as e:
            """
            EXCEPTION
            """
            return JsonResponse(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
