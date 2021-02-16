# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC75647f28d69ea248afba7325fc554d01'
auth_token = '0f7ca9a3e08adc10008de9151089f653'
client = Client(account_sid, auth_token)

call = client.calls.create(
                        twiml='<Response><Say>Ahoy, World!</Say></Response>',
                        to='+16039883806',
                        from_='+18283927597'
                    )

print(call.sid)