from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView



from .views import *

urlpatterns = [
    path('password/reset/confirm', 
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'
    ),
    path('password/reset/confirm/<uidb64>/<token>', 
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'
    ), 

    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/account_verification/<phone>', AccountVerification.as_view()),
]