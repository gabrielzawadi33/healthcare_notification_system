# myapp/utils.py
from django.conf import settings # type: ignore
# from twilio.rest import Client # type: ignore
from BeemAfrica import Authorize, SMS  # type: ignore


# def send_sms(to, body):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         body=body,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         to=to
#     )
#     print (message.sid)


import requests # type: ignore
import base64


def send_sms_via_beem(body, to):
    Authorize('6e44d2d63fe2bf20', 'Mzk3ODI4MDU0OTExNzUwMDVmYmJlZTdkOWYwM2ZjYzVmNjllNTM0ZGE0YjkyMTNhMGZkNzJmNGZiYTU3NTY0Yg==')

    response = SMS.send_sms(body, to, sender_id='HEALTHCARE')
    print(response)
    return response


# import africastalking # type: ignore

# # Initialize Africa's Talking in sandbox mode
# username = 'senders_username'
# api_key = 'senders_api_key'

# africastalking.initialize(username, api_key)

# # Get the SMS service
# sms = africastalking.SMS

# def send_smsA(to, message):
#     try:
#         # Send the SMS
#         response = sms.send(message, [to])
#         print(response)
#     except Exception as e:
#         print(f"Encountered an error while sending: {str(e)}")


