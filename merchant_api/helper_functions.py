import json

import bcrypt
import requests
from django.conf import settings
from django.core.cache import cache

from merchant.models import PasswordHistory
from merchant_api.models import JWTToken



def check_cache(f):
    def wrapper(*args, **kwargs):
        # check if cache contains access_token
        # and refresh_token keys
        
        if cache.get('ACCESS_TOKEN') is not None:        
            # get key values from cache
            # return access and refresh_token            
            return cache.get('ACCESS_TOKEN'), cache.get('REFRESH_TOKEN') 
        else:           
            # delegate task to the function
            return f()

    return wrapper


@check_cache
def get_jwt_tokens():
    # db queries to get tokens
    # store tokens in cacheas key value pairs     
    token = JWTToken.objects.filter(name='intelliPos').first()
    cache.set('ACCESS_TOKEN', token.access_token, settings.CACHE_EXPIRY)
    cache.set('REFRESH_TOKEN', token.refresh_token, settings.CACHE_EXPIRY)
    print(cache.get('ACCESS_TOKEN'))
    return token.access_token, token.refresh_token


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
