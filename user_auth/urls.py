from django.urls import path, include
from allauth.account import views 


from .views import *

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account_verification/<phone>', AccountVerification.as_view()),
]
