import datetime

import bcrypt
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from user_auth.models import User
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


class OperatorProfile(models.Model):
    """
    POS Operator Personal Profile
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    merchant = models.ForeignKey(
        MerchantProfile, 
        on_delete=models.CASCADE,
        related_name='operators'
    )

    def __str__(self):
        return f'{self.phone_number}'


class POSTerminal(models.Model):
    """
    Represents the Merchant POS Terminal
    where customer transactions take place
    """
    pos_id = models.CharField(max_length=20)
    last_logged_device = models.CharField(max_length=100)
    last_active = models.DateField(default=timezone.now)
    operator_profile = models.OneToOneField(
        OperatorProfile, 
        on_delete=models.SET_NULL,
        null=True
    )
    merchant = models.ForeignKey(
        MerchantProfile, 
        on_delete=models.CASCADE,
        related_name='pos_terminals'
    )
  
    def __str__(self):
        return f'{pos_id}'

    @property
    def operator(self):
        return self.operator_profile

    @operator.setter
    def operator(self, operator):
        """Sets POS Operator"""
        if operator:
            # get the operator instance using the
            # operator argument received in this function
            # assign the instance to our model property as shown below
            self.operator_profile = operator




class Transaction(models.Model):
    date = models.DateField(default=timezone.now)
    sender_account = models.CharField(max_length=30, default='', blank=True)
    receiver_account = models.CharField(max_length=30, default='', blank=True)
    destination_bank = models.CharField(max_length=50, default='', blank=True)
    amount = models.FloatField(default=0.00, blank=True)
    currency = models.CharField(max_length=255, default='USD', blank=True)
    reference = models.CharField(max_length=255, default='', blank=True)
    pos_terminal = models.ForeignKey(
        POSTerminal, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='transactions'
    )
