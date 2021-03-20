import requests
from django.conf import settings
from django.core.cache import cache


def login(username, password):
    r = requests.post(
        f'{settings.KMS_BASE_URL}/login', data={
            'username': username,
            'password': password
        }
    )
    # TODO: Use tests to handle behaviour when status code is not 200
    data = r.json()
    cache.set(
        'access_token',
        data['access_token'],
        settings.CACHE_JWT_EXPIRY
    )
    cache.set(
        'refresh_token',
        data['access_token'],
        settings.CACHE_JWT_EXPIRY
    )
    return data['access_token'], data['refresh_token']


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
        access_token, refresh_token = login(
            settings.KMS_USERNAME,
            settings.KMS_PASSWORD
        )
        # Save tokens in cache
        cache.set('access_token', access_token, settings.CACHE_JWT_EXPIRY)
        cache.set('refresh_token', access_token, settings.CACHE_JWT_EXPIRY)
        return access_token, refresh_token


class KMSCLIENTAPI:    
    KMS_BASE_URL = settings.KMS_BASE_URL
    ACCESS_TOKEN, REFRESH_TOKEN = get_jwt_tokens()

    def __init__(self):
        self._headers = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, token):
        self._headers = {'Authorization': f'Bearer {token}'}

    @check_dek_cache
    def request_dek(self, key_name):
        self.headers = KMSCLIENTAPI.ACCESS_TOKEN
        r = requests.get(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/keys/dek',
            headers=self.headers,
            params={'key_name': key_name}
        )
        data = r.json()
        if r.status_code == 200:  # Base behaviour
            data = r.json()
            dek = data['dek'].encode('ISO-8859-1')
            cache.set(key_name, dek, settings.CACHE_DEK_EXPIRY)
            return dek
        else:  # recursive behaviour
            print("Request DEK",r.status_code)
            print("Request DEK",r.json())
            KMSCLIENTAPI.ACCESS_TOKEN = self._refresh_token()
            dek = self.request_dek(key_name)
            return dek

    def _refresh_token(self):
        self.headers = KMSCLIENTAPI.REFRESH_TOKEN
        print("Refresh Token", self.headers)
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/token_refresh',
            headers=self.headers
        )
        print("Refresh DEK",r.status_code)
        print("Refresh DEK",r.json())
        # TODO: Use tests to handle behaviour when status code is not 200
        data = r.json()
        cache.set(
            'access_token',
            data['access_token'],
            settings.CACHE_JWT_EXPIRY
        )
        return data['access_token']
