from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """creates and saves a new user"""

        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email instead of username"""
    email = models.EmailField(_("email_address"), max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True)
    date_joined = models.DateField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

# class User(AbstractUser):
    #     """
#     IntelliPOS Merchant User Model
#     """
#     merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, null=True, blank=True)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     pass_hash = models.BinaryField()
#     otp = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20, default='263')
#     role = models.CharField(max_length=20, default='',
#                             choices=(('ADMIN', 'ADMIN'), ('TELLER', 'TELLER')))
#     pin_tries = models.IntegerField(default=3)
#     locked = models.BooleanField(default=False)
#     password_change = models.DateField(default=datetime.datetime.now() + datetime.timedelta(3 * 30))
#     unlocks_at = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=30))

#     def __str__(self):
#         return self.username

#     @classmethod
#     def get_user_by_username(cls, username):
#         return cls.objects.filter(username=username).first()

#     @classmethod
#     def email_availability(cls, email):
#         return cls.objects.filter(email=email).exists()

#     @classmethod
#     def generate_username(cls, first_name, last_name):
#         i = 0
#         username = first_name[0] + last_name
#         while cls.get_user_by_username(username=username):
#             username = first_name[0] + last_name + str(i)
#             i += 1
#         return username

#     @classmethod
#     def authenticate(cls, username, password):
#         user = User.objects.filter(username=username).first()
#         if user is None:
#             return False
#         if bcrypt.checkpw(password, user.password.encode("utf-8")):
#             return True
#         else:
#             return False


