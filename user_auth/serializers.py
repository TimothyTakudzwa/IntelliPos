from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from dj_rest_auth import serializers as ra_serializers
from django.conf import settings
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

from .models import User
from merchant.models import MerchantProfile
from .signals import user_failed_login

class UserDetailsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('email').read_only = True             # readonly exclusive to update

    class Meta:
        model = User
        fields = ('email',)


class LoginSerializer(ra_serializers.LoginSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)

        if not user:
            user_failed_login.send(sender=self.__class__, email=email)
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs


    

