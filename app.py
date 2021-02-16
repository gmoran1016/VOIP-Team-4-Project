from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import Play, VoiceResponse
from twilio.rest import Client
from gtts import gTTS

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()
    print(body)
    x = 0
    while x < 2:
        if 'number: ' in body:
            numberString = body
            number = numberString.removeprefix('number: ')
            resp.message("calling {}... ".format(number))
            x += 1
            return number
        elif 'message: ' in body:
            resp.message("message")
            message = body.removeprefix('message: ')
            print('Message ' + message)
            x+=1
            return message
        else:
            resp.message("error ")
    start(number, message)
    return str(resp)


def start(number, message):
    tts(message)
    call(number)


def tts(message):
    language = 'en'

    output = gTTS(text=message, lang=language, slow=False)
    output.save("output.mp3")


def call(number):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC75647f28d69ea248afba7325fc554d01'
    auth_token = '0f7ca9a3e08adc10008de9151089f653'
    client = Client(account_sid, auth_token)
    print(number)
    if '+1' not in number:
        number = "+1" + number

    call = client.calls.create(
        twiml='<Response><Play>output.mp3</play></Response>',
        to=number,
        from_='+18283927597'
    )

    print(call.sid)


if __name__ == "__main__":
    app.run(debug=True)
