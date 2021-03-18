import requests
from django.conf import settings
from merchant_api.helper_functions import get_jwt_tokens
from merchant_api.models import JWTToken
from json.decoder import JSONDecodeError


def check_cache(f):
    def wrapper(*args, **kwargs):
        # check if cache contains dek key
        if False:
            # get key value from cache
            # return dek value
            return
        else:
            # delegate task to the function
            return f(*args, **kwargs)

    return wrapper


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

    @check_cache
    def request_dek(self, key_name):
        self.headers = KMSCLIENTAPI.ACCESS_TOKEN
        r = requests.get(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/keys/dek',
            headers=self.headers,
            params={'key_name': key_name}
        )
        print(r)
        try:
            data = r.json()
        except JSONDecodeError as e:
            # KMS Application is down
            return 'Failed to get DEK'

        print('Response Data', data)
        # Base behaviour
        if r.status_code == 200:
            print(r)
            data = r.json()
            dek = data['dek'].encode('ISO-8859-1')
            # store dek in cache as key-value pair           
            return dek
        # recursive behavaiour        
        elif r.status_code == 401 and data['error']['code'] == '01':
            print(r)
            KMSCLIENTAPI.ACCESS_TOKEN = self._refresh_token()
            dek = self.request_dek(key_name)
            print(dek)
            return dek
        else:
            print(r)
            return 'Failed to get DEK'

    def _refresh_token(self):
        self.headers = KMSCLIENTAPI.REFRESH_TOKEN
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/token_refresh',
            headers=self.headers
        )
        data = r.json()
        token = JWTToken.objects.filter(access_token=KMSCLIENTAPI.ACCESS_TOKEN).first()
        token.access_token = data['access_token']
        token.save()
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
