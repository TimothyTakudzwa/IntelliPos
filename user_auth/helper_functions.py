import requests
from requests.auth import HTTPBasicAuth
from BulkSmsApi.Client import Client

# def send_otp(phone_number, otp):
#     message = f'<%23> ExampleApp: Your code is {otp} MoohrBwcY1d'

#     url = "https://mobile.esolutions.co.zw/bmg/api/single/ZB WhatsApp/" + \
#         phone_number + "/" + message
#     r = requests.get(url, auth=HTTPBasicAuth(
#         'ZBBANKAPI', 'kpACGdcj'), verify=False)
#     return ''

def send_otp(phone_number, otp):
    bulksms = Client('MarlvinzW', 'd59160bf797bda487639aa53a6103b05')
    message = f'<#> ExampleApp: Your code is {otp} MoohrBwcY1d' 
    bulksms.send(body=message, recipients=[phone_number])
    return ''
