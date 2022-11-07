#pip3 install flask
#pip3 install dialogflow
from flask import Flask
from flask import request, jsonify
import os
from google.cloud import dialogflow # this has been changed 
from google.api_core.exceptions import InvalidArgument
import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "private_key.json"

DIALOGFLOW_PROJECT_ID = "first-bot-o99c"
DIALOGFLOW_LANGUGAE_CODE = "en"
SESSION_ID = "akshat"

# app = Flask(__name__)
# app.config["DEBUG"] = True

# @app.route('/')
# def root():
#     return "Hello World"

# # @app.route('/api/getMessage',methods=['POST'])

def home():
    # message = request.form.get('Body') #meessage sent by the user
    # mobnum = request.form.get('From') # number of the user
    mobnum = "919457250831"
    message = "Hello"
    session_client = dialogflow.SessionsClient() # creating dialogflow session
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID) #configuring session
    text_input = dialogflow.TextInput(text = message, language_code = DIALOGFLOW_LANGUGAE_CODE) #
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input = query_input)
    except InvalidArgument:
        raise
    print("Query text:", response.query_result.query_text) # the text we just sent to the dialogflow
    print("Detected intent:", response.query_result.intent.display_name) # intent which it belongs to
    print("Detected intent confidence: ", response.query_result.intent_detection_confidence) #confidence
    print("fulfillment text:", response.query_result.fulfillment_text) # the response
    sendMessage(mobnum,response.query_result. fulfillment_text)
    return response.query_result. fulfillment_text
    
def sendMessage(mobnum,response):
    url = "https://iqwhatsapp.airtel.in/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/text"

    payload ={
        "sessionId" : "akshat",
        "to" : mobnum,
        "from" : "918904584255",
        "message" : {"text" : response}
    }

    headers = {
        'Authorization': 'Basic QUlSVEVMX0RJR192T0VsQUZxc0o4OVZoOXdxUVd4TDp6KkxVNktOPGt6c0w/K2JXMQ=='
    }

    response = requests.request("POST", url,headers=headers,json=payload)
    print(response.text.encode('utf-8'))
if  __name__ == '__main__':
    home()
    