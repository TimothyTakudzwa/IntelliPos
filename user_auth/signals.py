import logging
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from allauth.account.signals import user_logged_in
from django.conf import settings
from django.core.cache import cache

from .models import User

logger = logging.getLogger('gunicorn.error')

user_failed_login = Signal(providing_args=["email"])


@receiver(user_failed_login)
def hanlde_logon_attempt(sender, email, **kwargs):
    try:
        user = User.objects.get(email__exact=email)
    except User.DoesNotExist as e:
        logger.warn(e)
        return

    if  user.locked_out:
        return
    else:
        user.logon_attempts += 1
        user.save()

    if user.logon_attempts > settings.USER_ALLOWED_LOGON_ATTEMPTS:
        cache.set(
            user,
            user,
            settings.USER_LOCKOUT_DURATION 
        )


@receiver(user_logged_in)
def reset_login_attempts(request, user, **kwargs): 
    """
    Reset logon attempts after a successful logon following failed logon attempt(s)
    """
    if user.logon_attempts!=0:
        user.logon_attempts = 0
        user.save()
