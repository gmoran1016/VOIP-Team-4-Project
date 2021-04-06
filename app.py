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
1. Get Inputs Working correctly - Fixed
2. Fix Output.mp3 twiml error - Fixed but file needs to be hosted somewhere
3. Fix format code so number can be entered in any format
4. Upload to cloud service for deployment - Have an idea for this so should be good
5. Make sure it can handle multiple user at once. ( Probably can't do this at the moment)
6. Figure out tts file hosting solution.
"""

# Some Flask thing? IDK
@app.route("/sms", methods=['GET', 'POST'])
def bot():
    #Twilio Message Stuff
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    
    #Convert number to correct format to pass to twilio
    
    #variable
    i =0
    
    
    #Checks for the /s to start the program by asking for the number. Should increment through steps but currently doesnt
    if '/s' in incoming_msg:
        msg.body('Please enter a number in +15554443333 format:')
        print(resp)
    elif '+1' in incoming_msg:
        
        storeNumber(incoming_msg)
        msg.body('Please type /m then enter you message')
            
    elif '/m' in incoming_msg:
        storeMessage(incoming_msg)
        call()       
    else:
        msg.body('Please Begin by sending /s')

    return str(resp)

def storeNumber(number):
    storeNumber.numberResp = "'"+number+"'"
    print(storeNumber.numberResp)

def storeMessage(message):
    if '/m' in message:
        print(message)
        storeMessage.messageResp = message[2:]
        print(storeMessage.messageResp)
    else:
        print('Error in message')
       
    
    
# Does the TTS Magic and saves as output.mp3 in root folder
def tts(message):
    language = 'en'

    output = gTTS(text=message, lang=language, slow=False)
    output.save("files/output.mp3")


# Does the calling
def call():
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'AC75647f28d69ea248afba7325fc554d01'
    auth_token = '0f7ca9a3e08adc10008de9151089f653'
    client = Client(account_sid, auth_token)
    print(storeNumber.numberResp)
    # makes sure number has US Code at beginning. Need to make this better in case of formatting issues
    #Redundant Currently
    if '+1' not in storeNumber.numberResp:
        storeNumber.numberResp = "+1" + storeNumber.numberResp
    # Creates the call client and twiml needed to call via Twilio
    print('call time'+' '+storeNumber.numberResp+' '+storeMessage.messageResp)
    call = client.calls.create(
        twiml='<Response>'
              '<Say>'+storeMessage.messageResp+'</Say>'
              '</Response>',
        to=storeNumber.numberResp,
        from_='+18283927597'
    )

    print(call.sid)


if __name__ == "__main__":
    app.run()
