from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings

from .models import User
from merchant.models import MerchantProfile


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        read_only_fields = ('email',)
        extra_kwargs = {'password': {'write_only': True}}


class RegistrationSerializer(RegisterSerializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    is_merchant_admin = serializers.BooleanField(default=False)

    def validate_is_merchant_admin(self, is_merchant_admin):
        if not isinstance(is_merchant_admin, bool):
            raise serializers.ValidationError(_("is_merchant_admin should be True/False"))
        return is_merchant_admin


    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'is_merchant_admin': self.validated_data.get('is_merchant_admin', '')

        }
