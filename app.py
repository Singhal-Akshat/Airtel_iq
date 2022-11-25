#pip3 install flask
#pip3 install google-cloud-dialogflow
import os
from flask import Flask
from flask import  jsonify, request
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow  # this has been changed
from google.protobuf.json_format import MessageToDict
from send import sendMessage
from generate import generate_type
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_key.json"

DIALOGFLOW_PROJECT_ID = "newagent-xojq"
DIALOGFLOW_LANGUGAE_CODE = "en"


app = Flask(__name__)
app.config["DEBUG"] = True

flag = False

@app.route('/')
def root():
    return "Hello World"

@app.route('/api/getMessage',methods=['POST'])
def home():

    r = request.get_json()
    print(r)
    
    if(check_time(r)): # if time greater than 120 seconds return
        return ''

    sessionId = r['sessionId']
    mobnum = r['from']
    type = r['message']['type']
    message = ""

    if type=='text':
        message = r['message']['text']['body']
    else:
        itype = r['message'][type]['type']
        message = r['message'][type][itype]['title']

    print(message, mobnum)

    session_client = dialogflow.SessionsClient() # creating dialogflow session
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, sessionId) #configuring session
    text_input = dialogflow.TextInput(text = message, language_code = DIALOGFLOW_LANGUGAE_CODE) #
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input = query_input)
    except InvalidArgument:
        raise
    
    response2 = MessageToDict(response._pb)
    param = response2['queryResult']['parameters']
    print(param)
    
    print("Query text:", response.query_result.query_text) # the text we just sent to the dialogflow
    print("Detected intent:", response.query_result.intent.display_name) # intent which it belongs to
    print("Detected intent confidence: ", response.query_result.intent_detection_confidence) #confidence
    print("fulfillment text:", response.query_result.fulfillment_text) # the response

    intent_name = response.query_result.intent.display_name
    res = response.query_result.fulfillment_text

    if(intent_name == ''):
        ob = sendMessage(mobnum,sessionId)
        ob.text(res)
    
    type = intent_name.split('_')[0]
    print(type)
    o = generate_type(res,sessionId,mobnum,intent_name,param)
    o.find(type)
   
    return response.query_result. fulfillment_text

def check_time(r):
    time_stamp = time.time()
    tm= float(r['message']['timestamp'])
    tm = tm/1000
    delta = time_stamp - tm
    if(delta > 120) :
        return True
    return False

if  __name__ == '__main__':
    app.run()    