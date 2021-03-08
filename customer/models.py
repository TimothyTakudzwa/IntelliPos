from django.db import models
from merchant.models import Account
import bcrypt 


# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=255, default='')
    nfc_token = models.CharField(max_length=255, default='', blank=True)
    nfc_pin = models.TextField(max_length=255,blank=True, null=True)
    card_number = models.TextField(max_length=20,blank=True, null=True)
    card_pin = models.TextField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=255, default='')
    is_verified = models.BooleanField(default=False, blank=True)
    initial_balance = models.IntegerField(default=0)

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='customer_account')

    def __str__(self):
        return self.customer_name

    @classmethod
    def get_user_by_nfc_token(cls, nfc_token):
        return cls.objects.filter(nfc_token=nfc_token).first()

    @classmethod
    def get_user_by_card_number(cls, card_number):
        return cls.objects.filter(card_number=card_number).first()

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    @classmethod
    def authenticate(cls, customer, nfc_token, nfc_pin, transType):
        try:
            
            if transType == 'NFC':
                pin = customer.nfc_pin                
            else:
                pin = customer.card_pin    
                   
            if bcrypt.checkpw(nfc_pin.encode("utf-8"), pin.encode("utf-8")):
                return True
            else:
                return False
        except Exception as e:
            print(f'\n EXCEPTION : \n {e} \n')
            return False

    @classmethod
    def set_pin(cls, nfc_token, pin):
        user = cls.get_user_by_nfc_token(nfc_token)
        user.nfc_pin = cls.hash_password(pin).decode('utf8')
        user.save()