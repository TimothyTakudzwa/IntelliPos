
from django.conf import settings
from allauth.account import app_settings as allauth_settings
from rest_auth.registration.views import RegisterView
from rest_auth.app_settings import (
    TokenSerializer,
    JWTSerializer,
    create_token
)
from rest_framework import status, viewsets
from rest_framework.response import Response

logger = logging.getLogger('gunicorn.error')
class RegisterView(RegisterView):
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent."), "token": self.token}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            logger.info('Successfully Registered User')
            return JWTSerializer(data).data
        else:
            logger.info('Successfully Registered User')
            return TokenSerializer(user.auth_token).data