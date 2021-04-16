from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from gtts import gTTS
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "Voip.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")
        
    app.run(host="0.0.0.0", port=8008, debug=False)

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
    account_sid = 'AC75647f28d69ea248afba7325fc554d01'
    auth_token = '0f7ca9a3e08adc10008de9151089f653'
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
    main()
