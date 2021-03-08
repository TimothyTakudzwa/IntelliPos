
from .models import JWTToken
import json 
import requests

def get_access_token(name):
    token = JWTToken.objects.filter(name=name).first()
    if token is None:
        url = 'http://45.55.44.41:8003/api/v1/register'
        data = {'username' : 'takudzwatimothy', 'password' : '12345'}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print('-------------------------------------')
        print(r.json())
        print('-------------------------------------')

        data = r.json()
        token = JWTToken(access_token=data['access_token'], refresh_token=data['refresh_token'], name=name)
        token.save()
    return token.access_token