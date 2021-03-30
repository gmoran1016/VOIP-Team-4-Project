# VOIP-Team-4-Project

CURRENT STATUS:

app.py- Program needs to wait for both the number and message to be received before calling start. This doesnt work currently.
Currently will take any message sent to the number and convert it to a number and try to call it which doesnt work unless the message you send is a phone number.
At which point it will just change the phone number to speech call successfully and then fail to read output.mp3.

TODO:
1. Get Inputs Working correctly - Fixed
2. Fix Output.mp3 twiml error - Fixed but file needs to be hosted somewhere
3. Fix format code so number can be entered in any format
4. Upload to cloud service for deployment - Have an idea for this so should be good
5. Make sure it can handle multiple user at once. ( Probably can't do this at the moment)
6. Figure out tts file hosting solution.
