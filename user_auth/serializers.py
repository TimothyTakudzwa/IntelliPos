import datetime
from django.contrib.auth.hashers import check_password
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from dj_rest_auth import serializers as ra_serializers
from django.conf import settings


from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode as uid_decoder
try:
    from django.utils.translation import gettext_lazy as _
except ImportError:
    from django.utils.translation import gettext_lazy as _

from .models import User, PasswordArchive
from merchant.models import MerchantProfile
from .signals import user_failed_login


# Get the UserModel
UserModel = get_user_model()

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


class PasswordChangeSerializer(ra_serializers.PasswordChangeSerializer):

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def validate_new_password1(self, value):
        # Is password recently used?
        password_archive = PasswordArchive.objects.find_all_for(self.user)
        password_check = check_password(value, self.user.password)        
        if any([check_password(value, entry.password_hash) for entry in password_archive]) or password_check:  
            err_msg = _("Your new entered password was recently used. Please use a new password.")          
            raise serializers.ValidationError(err_msg)
        return value


    def save(self):
        PasswordArchive.objects.create(                 # archive old password before changing to new password
            password_hash=self.user.password, 
            user=self.user
        )
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)

        self.user.password_date_created = datetime.datetime.now()    # date when new password was created


class PasswordResetConfirmSerializer(ra_serializers.PasswordResetConfirmSerializer):

    def validate(self, attrs):

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        # Is password recently used?
        password_archive = PasswordArchive.objects.find_all_for(self.user)
        password_check = check_password(attrs['new_password1'], self.user.password)        
        if any([check_password(attrs['new_password1'], entry.password_hash) for entry in password_archive]) or password_check:  
            err_msg = _("Your new entered password was recently used. Please use a new password.")          
            raise serializers.ValidationError({'new_password':err_msg})

        return attrs
