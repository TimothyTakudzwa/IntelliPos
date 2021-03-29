import logging
import requests
from django.conf import settings
from django.core.cache import cache

from .helper_functions import check_dek_cache, get_jwt_tokens

logger = logging.getLogger('gunicorn.error')


class KMSCLIENTAPI:    
    """
    Class used to represent the KMS Client API.

    Attributes
    ----------
    headers : str
        HTTP Headers for the requests
    KMS_BASE_URL : str
        api server base url for requests
    acess_token : str
        jwt access token
    refresh_token : str
        jwt refresh token

    Methods
    -------
    request_dek(key_name)
        Gets Data Encryption Key

    refresh_token()
        Refreshes access token

    login(username, password)
        Performs login to get new tokens
    """
    
    KMS_BASE_URL = settings.KMS_BASE_URL
    access_token, refresh_token = get_jwt_tokens()

    def __init__(self):
        self._headers = None


    @property
    def headers(self):
        return self._headers


    @headers.setter
    def headers(self, token):
        """Sets HTTP headers for the request"""
        token, refresh = token
        if token is None:
            access_token, refresh_token = KMSCLIENTAPI.login(
                settings.KMS_USERNAME,
                settings.KMS_PASSWORD
            )
            token = refresh_token if refresh else access_token
        self._headers = {'Authorization': f'Bearer {token}'}


    @check_dek_cache
    def request_dek(self, key_name):
        """Gets and returns DEK"""
        self.headers = (KMSCLIENTAPI.access_token, False)
        r = requests.get(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/keys/dek',
            headers=self.headers,
            params={'key_name': key_name}
        )
        data = r.json()
        if r.status_code == 200: 
            data = r.json()
            dek = data['dek'].encode('ISO-8859-1')
            cache.set(key_name, dek, settings.CACHE_DEK_EXPIRY)
            logger.info('Sent Successful DEK Request to KMS')
            return dek
        else:  
            KMSCLIENTAPI.access_token = self._refresh_token()
            dek = self.request_dek(key_name)
            return dek
            

    def _refresh_token(self):
        """Gets and returns new access token"""
        self.headers = (KMSCLIENTAPI.refresh_token, True)
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/token_refresh',
            headers=self.headers
        )
        data = r.json()
        cache.set(
            'access_token',
            data['access_token'],
            settings.CACHE_JWT_EXPIRY
        )
        return data['access_token']


    def login(username, password):
        """Login and returns new JWT tokens"""
        r = requests.post(
            f'{settings.KMS_BASE_URL}/login', data={
                'username': username,
                'password': password
            })
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
        logger.info('KMS Client Login - Acquired access and refresh tokens')
        return data['access_token'], data['refresh_token']