import bcrypt
from django.conf import settings
from django.core.cache import cache

from merchant.kms_client_api import KMSCLIENTAPI


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