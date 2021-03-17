import requests

class KMSCLIENTAPI:
    KMS_BASE_URL = 'http://45.55.44.41:8003/api/v1'

    def __init__(self, access_token=None, token_refresh=None):
        self.headers = {
            'Authorization': (
                f'Bearer  '
                f'{access_token if access_token else token_refresh}'
            )
        }

    def request_dek(self, key_name):
        r = requests.get(

            f'{KMSCLIENTAPI.KMS_BASE_URL}/keys/dek',
            headers=self.headers,
            params = {'key_name':key_name}
        )
    

    def refresh_token(self):
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/token_refresh',
            headers = self.headers
        )

    @staticmethod
    def login(username, password):
        r = requests.post(
            f'{KMSCLIENTAPI.KMS_BASE_URL}/login', data = {
                'username':username, 
                'password':password
            }
        )


# Usage

# Get DEK
# dek = KMSCLIENTAPI(access_token=access_token).request_dek(key_name)

# Refresh Token
# refresh_token = KMSCLIENTAPI(token_refresh=token).refresh_token()

# # Login
# access_token, refresh_token = KMSCLIENTAPI.login(username, password)