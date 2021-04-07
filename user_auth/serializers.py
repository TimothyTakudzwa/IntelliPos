from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings

from .models import User
from merchant.models import MerchantProfile


class UserDetailsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('email').read_only = True             # readonly exclusive to update

    class Meta:
        model = User
        fields = ('email',)



    

