from django.urls import path, include
from allauth.account import views 


from .views import *

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    # path('auth/registration/', include('rest_auth.registration.urls'))
    path('auth/registration/', RegisterView.as_view(), name='register'),
]
