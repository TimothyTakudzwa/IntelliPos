import datetime

import bcrypt
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from .constants import BANKS, INDUSTRY_CHOICES, COMPANY_TYPE


# Create your models here.


class Account(models.Model):
    """ 
    Merchant Account Model 
    """
    account_number = models.CharField(max_length=30)
    balance = models.FloatField(default=0, blank=True)
    destination_bank = models.CharField(max_length=100, default='', choices=BANKS)

    def __str__(self):
        return f'{self.account_number}'


class Merchant(models.Model):
    """
    IntelliPOS Merchant Model
    """
    name = models.CharField(max_length=100, default='', unique=True)
    address = models.CharField(max_length=255, default='')
    email = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=30, default='')
    industry = models.CharField(max_length=100, default='', choices=INDUSTRY_CHOICES)
    company_type = models.CharField(max_length=30, default='', choices=COMPANY_TYPE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='merchant_account', blank=True)

    def __str__(self):
        return f'{str(self.id)} - {str(self.name)} {str(self.address)}'

    @classmethod
    def get_model_by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def get_merchant_by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def update_merchant(cls, name, address, email, phone_number):
        merchant = cls.get_merchant_by_name(name)
        merchant.address = address
        merchant.email = email
        merchant.phone_number = phone_number
        merchant.save()


class User(AbstractUser):
    """
    IntelliPOS Merchant User Model
    """
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pass_hash = models.BinaryField()
    otp = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, default='263')
    role = models.CharField(max_length=20, default='',
                            choices=(('ADMIN', 'ADMIN'), ('TELLER', 'TELLER')))
    pin_tries = models.IntegerField(default=3)
    locked = models.BooleanField(default=False)
    password_change = models.DateField(default=datetime.datetime.now() + datetime.timedelta(3 * 30))
    unlocks_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=30))

    def __str__(self):
        return self.username

    @classmethod
    def get_user_by_username(cls, username):
        return cls.objects.filter(username=username).first()

    @classmethod
    def email_availability(cls, email):
        return cls.objects.filter(email=email).exists()

    @classmethod
    def generate_username(cls, first_name, last_name):
        i = 0
        username = first_name[0] + last_name
        while cls.get_user_by_username(username=username):
            username = first_name[0] + last_name + str(i)
            i += 1
        return username

    @classmethod
    def authenticate(cls, username, password):
        user = User.objects.filter(username=username).first()
        if user is None:
            return False
        if bcrypt.checkpw(password, user.password.encode("utf-8")):
            return True
        else:
            return False


class PasswordHistory(models.Model):
    """
    Model Class to save the last 4 password of a merchant
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    password_hash_1 = models.TextField(blank=True, null=True)
    password_hash_2 = models.TextField(blank=True, null=True)
    password_hash_3 = models.TextField(blank=True, null=True)
    password_hash_4 = models.TextField(blank=True, null=True)
    next_cycle = models.IntegerField(default=1)


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
            time_difference =user.unlocks_at.replace(tzinfo=None) - datetime.datetime.now().replace(tzinfo=None)
            minutes = time_difference.seconds//60
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
                print('TEST')
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
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, blank=False, null=False)
    pos = models.ForeignKey(IntelliPos, on_delete=models.PROTECT, related_name='writer_merchant')
    status = models.BooleanField(default=False)
