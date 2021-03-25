import requests
from requests.auth import HTTPBasicAuth

def send_sms(phone_number, message):
    url = "https://mobile.esolutions.co.zw/bmg/api/single/ZB WhatsApp/" + \
        phone_number + "/" + message
    r = requests.get(url, auth=HTTPBasicAuth(
        'ZBBANKAPI', 'kpACGdcj'), verify=False)
    return ''