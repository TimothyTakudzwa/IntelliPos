from django.urls import path, include
from dj_rest_auth.views import (
    PasswordResetConfirmView
)


from .views import *

urlpatterns = [
    path('password/reset/confirm/<uidb64>/<token>', 
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ), 
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account_verification/<phone>', AccountVerification.as_view()),
]
