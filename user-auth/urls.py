from django.urls import path, include
from allauth.account import views 


urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls'))
]
