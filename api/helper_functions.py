import json

import requests

from merchant.models import PasswordHistory
from .models import JWTToken


def password_used(user, new_password):
    history = PasswordHistory.objects.filter(user=user).first()
    if history is None:
        PasswordHistory(user=user, password_hash_1=user.password_hash).save()
        return False
    else:
        if history.password_hash_1 == new_password:
            return True
        elif history.password_hash_2 == new_password:
            return True
        elif history.password_hash_3 == new_password:
            return True
        elif history.password_hash_4 == new_password:
            return True
        else:
            save_to_history(user, history)
            return True


def save_to_history(user, history):
    if history.next_clycle == 1:
        history.password_hash_1 = user.password_hash
    elif history.next_clycle == 1:
        history.password_hash_2 = user.password_hash
    elif history.next_clycle == 1:
        history.password_hash_3 = user.password_hash
    elif history.next_clycle == 1:
        history.password_hash_4 = user.password_hash
    history.save()
    return True


def get_access_token(name):
    token = JWTToken.objects.filter(name=name).first()
    if token is None:
        url = 'http://45.55.44.41:8003/api/v1/register'
        data = {'username': 'takudzwatimothy', 'password': '12345'}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print('-------------------------------------')
        print(r.json())
        print('-------------------------------------')

        data = r.json()
        token = JWTToken(access_token=data['access_token'], refresh_token=data['refresh_token'], name=name)
        token.save()
    return token.access_token
