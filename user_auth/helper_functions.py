import requests
from requests.auth import HTTPBasicAuth
from intelli_sms_gateway.client import Client
# def send_otp(phone_number, otp):
#     message = f'<%23> ExampleApp: Your code is {otp} MoohrBwcY1d'

#     url = "https://mobile.esolutions.co.zw/bmg/api/single/ZB WhatsApp/" + \
#         phone_number + "/" + message
#     r = requests.get(url, auth=HTTPBasicAuth(
#         'ZBBANKAPI', 'kpACGdcj'), verify=False)
#     return ''
client = Client('mgunityrone@gmail.com', '123abc!!!')

def send_otp(phone_number, otp):
    message = f'IntelliPOS: Your code is {otp} MoohrBwcY1d' 
    client.send_single_sms(message, phone_number, 'IntelliPos')

    return ''
