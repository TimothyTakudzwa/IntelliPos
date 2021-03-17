import requests
from django.conf import settings
from merchant_api.helper_functions import get_jwt_token


class KMSCLIENTAPI:
    KMS_BASE_URL = settings.KMS_BASE_URL
    ACCESS_TOKEN, REFRESH_TOKEN = get_jwt_token()

    def __init__(self):
        self._headers = None

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, token):
        self._headers = {'Authorization': f'Bearer {token}'}

   
    def request_dek(self, key_name):
        self.headers = KMSCLIENTAPI.ACCESS_TOKEN
        r = requests.get(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/keys/dek',
            headers=self.headers,
            params={'key_name': key_name}
        )
        data = r.json()
        # Base behaviour
        if r.status_code == 200:
            data = r.json()
            dek = data['dek'].encode('ISO-8859-1')
            return dek
        # recursive behavaiour        
        elif r.status_code == 401 and data['error']['code']=='01':
            KMSCLIENTAPI.ACCESS_TOKEN = self._refresh_token()
            self.request_dek(key_name)

    
        
    def _refresh_token(self):
        self.headers = KMSCLIENTAPI.REFRESH_TOKEN
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/token_refresh',
            headers=self.headers
        )
        data = r.json()
        return data['access_token']

    @staticmethod
    def login(username, password):
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/login', data={
                'username': username,
                'password': password
            }
        )
        return r

# Usage

# Get DEK
# dek = KMSCLIENTAPI(token=token).request_dek(key_name)

# # Login
# access_token, refresh_token = KMSCLIENTAPI.login(username, password)
