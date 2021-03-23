from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from merchant import views
from .views import *

router = routers.DefaultRouter()
# router.register(r'users', RegisterViewSet)
# router.register(r'transactions', TransactionViewSet )

urlpatterns = [
    path('', include(router.urls)),

]

