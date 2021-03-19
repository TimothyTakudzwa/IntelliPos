import bcrypt
from django.conf import settings
from django.core.cache import cache

from .models import PasswordHistory


def check_dek_cache(f):
    """
    Decorator function for checking if cache contains the requested DEK
    """

    def wrapper(*args):
        _, key_name = args
        if cache.has_key(key_name):
            return cache.get(key_name)
        else:
            return f(*args)

    return wrapper


def get_jwt_tokens():
    """
    Gets JWT tokens from cache or KMS server
    """
    if cache.has_key('access_token') and cache.has_key('refresh_token'):
        tokens = cache.get_many(['access_token', 'refresh_token'])
        return tokens['access_token'], tokens['refresh_token']
    else:
        # Login
        access_token, refresh_token = KMSCLIENTAPI.login(
            settings.KMS_USERNAME,
            settings.KMS_PASSWORD
        )
        # Save tokens in cache
        cache.set('access_token', access_token, settings.TOKEN_CACHE_EXPIRY)
        cache.set('refresh_token', access_token, settings.TOKEN_CACHE_EXPIRY)
        return access_token, refresh_token


def password_used(user, new_password):
    history = PasswordHistory.objects.filter(user=user).first()
    password = b"super secret password"
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if bcrypt.checkpw(new_password, user.password.encode("utf-8")):
        return True
    if history is None:
        PasswordHistory(user=user, password_hash_1=user.password).save()
        return False
    else:
        if bcrypt.checkpw(new_password, history.password_hash_1.encode("utf-8")):
            return True
        elif bcrypt.checkpw(new_password, history.password_hash_2.encode("utf-8")):
            return True
        elif bcrypt.checkpw(new_password, history.password_hash_3.encode("utf-8")):
            return True
        elif bcrypt.checkpw(new_password, history.password_hash_4.encode("utf-8")):
            return True
        else:
            save_to_history(user, history)
            return True


def save_to_history(user, history):
    if history.next_cycle == 1:
        history.password_hash_1 = user.password
        history.next_cycle = 2
    elif history.next_cycle == 2:
        history.password_hash_2 = user.password
        history.next_cycle = 3
    elif history.next_cycle == 3:
        history.password_hash_3 = user.password
        history.next_cycle = 4
    elif history.next_cycle == 4:
        history.password_hash_4 = user.password
        history.next_cycle = 1
    history.save()
    return True
