from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gtts import gTTS

app = Flask(__name__)

"""
CURRENT STATUS:

Program needs to wait for both the number and message to be received before calling start. This doesnt work 
currently. Currently will take any message sent to the number and convert it to a number and try to call it which 
doesnt work unless the message you send is a phone number. At which point it will just change the phone number to 
speech call successfully and then fail to read output.mp3. 

TODO:
1. Get Inputs Working correctly
2. Fix Output.mp3 twiml error
3. Fix format code so number can be entered in any format
4. Upload to cloud service for deployment
5. Make sure it can handle multiple user at once. ( Probably can't do this at the moment)
"""


# Some Flask thing? IDK
@app.route("/sms", methods=['GET', 'POST'])
# gets incoming SMS and does the main stuff, Doesn't work fully yet
def incoming_sms():
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()
    print(body)
    # supposed to send a text asking for number when any message is received.
    resp.message("Enter Target Phone number in format +15554443333")
    # old number syntax can probably remove
    number = body.removeprefix('number: ')
    # Supposed to then send a text prompting for the message.
    resp.message("Please enter the message to be converted")
    # old Message syntax can probably remove
    message = body.removeprefix('message: ')

    # resp.message("calling {}... ".format(number))
    start(number, message)
    return str(resp)


# supposed to call everything? IDK
def start(number, message):
    tts(message)
    call(number)


# Does the TTS Magic and saves as output.mp3 in root folder
def tts(message):
    language = 'en'

    output = gTTS(text=message, lang=language, slow=False)
    output.save("output.mp3")


# Does the calling
def call(number):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC75647f28d69ea248afba7325fc554d01'
    auth_token = '0f7ca9a3e08adc10008de9151089f653'
    client = Client(account_sid, auth_token)
    print(number)
    # makes sure number has US Code at beginning. Need to make this better in case of formatting issues
    if '+1' not in number:
        number = "+1" + number
    # Creates the call client and twiml needed to call via Twilio
    call = client.calls.create(
        twiml='<Response>'
              '<Play>output.mp3</play>'
              '</Response>',
        to=number,
        from_='+18283927597'
    )

    print(call.sid)


if __name__ == "__main__":
    app.run(debug=True)
