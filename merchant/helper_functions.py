import bcrypt
from django.conf import settings
from django.core.cache import cache


def check_dek_cache(f):
    """
    Decorates KMSAPIClient request dek function
    Checks if cache contains the requested DEK
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
    Gets and returns JWT tokens from cache
    """
    try:
        tokens = cache.get_many(['access_token', 'refresh_token'])
        return tokens['access_token'], tokens['refresh_token']
    except KeyError as e:
        return None, None
