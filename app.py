from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gtts import gTTS

app = Flask(__name__)

# Some Flask thing? IDK
@app.route("/sms", methods=['GET', 'POST'])
def bot():
    
    #Twilio Message Stuff
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    
    #Checks for the start command
    if '/s' in incoming_msg:
        msg.body('Please enter a number in +15554443333 format:')
    
    #Checks for phone number based on if it has 10 digits or starts with +!  
    elif '+1' in incoming_msg or len(incoming_msg) == 10 :
        if len(incoming_msg) == 10:
            fixed = '+1'+incoming_msg
            
            storeNumber(fixed)
            msg.body('Please type /m then enter you message')
        else:    
            storeNumber(incoming_msg)
            msg.body('Please type /m then enter you message')
    
    #Checks for the message to be sent        
    elif '/m' in incoming_msg:
        storeMessage(incoming_msg)
        tts()
    
    #in case of error
    else:
        msg.body('Please Begin by sending /s')

    return str(resp)

#Stores Number for later
def storeNumber(number):
    storeNumber.numberResp = "'"+number+"'"
    
#Stores Message for later
def storeMessage(message):
    if '/m' in message:
        
        storeMessage.messageResp = message[2:]
        
    else:
        print('Error in message')

    
# Does the TTS Magic and saves as output.mp3 in root folder
def tts():
    language = 'en'

    output = gTTS(text=storeMessage.messageResp, lang=language, slow=False, tld='ie')
    output.save("files/output.mp3")
    print("TTS Success")
    call()


# Does the calling
def call():
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    
    # makes sure number has US Code at beginning. Need to make this better in case of formatting issues
    if '+1' not in storeNumber.numberResp:
        storeNumber.numberResp = "+1" + storeNumber.numberResp
    
    # Creates the call client and twiml needed to call via Twilio
    print('call time'+' '+storeNumber.numberResp+' '+storeMessage.messageResp)
    
    #twiml Response
    call = client.calls.create(
        twiml='<Response>'
              '<Play>http://3.138.194.186:8000/output.mp3</Play>'
              '</Response>',
        to=storeNumber.numberResp,
        from_='+18283927597'
    )
    
    print(call.sid)

#starts the app on port 8008
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=False)
