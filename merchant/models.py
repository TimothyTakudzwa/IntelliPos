import datetime

import bcrypt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from .constants import BANKS
from .crypto import NISTApprovedCryptoAlgo
from .kms_client_api import KMSCLIENTAPI


class MerchantProfile(models.Model):
    """
    Merchant Business Profile
    """

    name = models.CharField(max_length=100, unique=True)
    country = CountryField()
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_model_by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def get_by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def update_merchant(cls, name, address, email, phone_number):
        merchant = cls.get_merchant_by_name(name)
        merchant.address = address
        merchant.email = email
        merchant.phone_number = phone_number
        merchant.save()


class BankAccount(models.Model):
    """ 
    Merchant Bank Account Details 
    """
    account_number = models.CharField(max_length=30)
    destination_bank = models.CharField(max_length=100, default='', choices=BANKS)
    merchant = models.ForeignKey(
        MerchantProfile,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )

    @property
    def masked_account_number(self):
        """
        Masks account number to only show the last N digits
        """
        pass

    def __str__(self):
        return f'{self.account_number}'


# class PasswordHistory(models.Model):
    """
    Model Class to save the last 4 password of a merchant
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    password_hash = models.BinaryField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    @classmethod
    def get_user_history(cls, user):
        return cls.objects.filter(user=user).order_by('-date')[:4].all()

    @staticmethod
    def password_used(user, password):
        history = PasswordHistory.get_user_history(user)
        if history is not None:
            PasswordHistory(password_hash=password, user=user).save()
            return False
        else:
            for inst in history:
                dek = KMSCLIENTAPI().request_dek('token_key')
                plain_text = NISTApprovedCryptoAlgo['AES'].value.handle_ct(dek, inst.password)
                if plain_text == password:
                    return True
                else:
                    PasswordHistory(password_hash=inst.password, user=user).save()
                    return False


class IntelliPos(models.Model):
    """
    Merchant IntelliPOS Model
    """
    pos_id = models.CharField(max_length=20, default='')
    last_logged_device = models.CharField(max_length=255)
    last_active_time = models.CharField(max_length=255)
    active_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, blank=False, null=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.id)} - {str(self.pos_id)}'

    @classmethod
    def authenticate(cls, username, password, posId, device):
        user = User.objects.filter(username=username).first()
        if user is None:
            return False, 'Username does not exist'
        if user.locked:
            time_difference = user.unlocks_at.replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)
            minutes = time_difference.seconds // 60
            print(minutes)
            if minutes < 30:
                return False, 'This Account is Locked'
            else:
                user.locked = False
                user.pin_tries = 3
                user.save()
        if user.password_change < datetime.date.today():
            return False, 'Password has expired'
        pos = cls.objects.filter(pos_id=posId).filter(merchant=user.merchant).first()
        if pos is None:
            return False, 'Invalid POS ID'
        if bcrypt.checkpw(password, user.password.encode("utf-8")):
            pos.active_user = user
            pos.last_logged_device = device
            pos.last_active_time = datetime.datetime.now()
            pos.is_logged_in = True
            pos.save()
            return True, 'Login Successful'
        else:
            user.pin_tries = user.pin_tries - 1
            if user.pin_tries < 1:
                user.pin_tries = 0
                user.locked = True
                user.unlocks_at = datetime.datetime.now() + datetime.timedelta(minutes=30)
            user.save()
            return False, 'Wrong username / password'


class Transaction(models.Model):
    date = models.DateField(default=timezone.now)
    sender_account = models.CharField(max_length=30, default='', blank=True)
    receiver_account = models.CharField(max_length=30, default='', blank=True)
    destination_bank = models.CharField(max_length=50, default='', blank=True)
    amount = models.FloatField(default=0.00, blank=True)
    currency = models.CharField(max_length=255, default='USD', blank=True)
    reference = models.CharField(max_length=255, default='', blank=True)
    merchant = models.ForeignKey(MerchantProfile, on_delete=models.CASCADE, blank=False, null=False)
    pos = models.ForeignKey(IntelliPos, on_delete=models.PROTECT, related_name='writer_merchant')
    status = models.BooleanField(default=False)
