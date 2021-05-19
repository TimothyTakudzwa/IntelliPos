import requests
from requests.auth import HTTPBasicAuth

def send_otp(phone_number, otp):
    message = f'<%23> ExampleApp: Your code is {otp} MoohrBwcY1d'

    url = "https://mobile.esolutions.co.zw/bmg/api/single/ZB WhatsApp/" + \
        phone_number + "/" + message
    r = requests.get(url, auth=HTTPBasicAuth(
        'ZBBANKAPI', 'kpACGdcj'), verify=False)
    return ''