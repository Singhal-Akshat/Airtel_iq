#pip3 install flask
#pip3 install google-cloud-dialogflow
import os
import requests
from flask import Flask
from flask import  jsonify, request
from google.api_core.exceptions import InvalidArgument
from google.cloud import dialogflow  # this has been changed
from google.protobuf.json_format import MessageToDict
import csv
import json
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
# @app.route('/test',methods=['POST'])
def home():

    r = request.get_json()
    print(r)
    
    # time_stamp = time.time()
    # print(time_stamp)
    # tm= float(r['message']['timestamp'])
    # tm = tm/1000
    # print(tm)
    # delta = time_stamp - tm
    # if(delta > 120) :
    #     return ""

    # global flag
    # print(flag)
    sessionId = r['sessionId']
    mobnum = r['from']
    type = r['message']['type']
    message = ""
    if type=='text':
        message = r['message']['text']['body']
    else:
        itype = r['message'][type]['type']
        # if itype == 'list_reply':
        #     message = r['message'][type][itype]['description']
        # else :
        message = r['message'][type][itype]['title']

    # if flag == True:
    #     train_list(message,sessionId,mobnum)
    #     flag = False
    #     return ""
    print(message, mobnum)
    session_client = dialogflow.SessionsClient() # creating dialogflow session
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, sessionId) #configuring session
    text_input = dialogflow.TextInput(text = message, language_code = DIALOGFLOW_LANGUGAE_CODE) #
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input = query_input)
    except InvalidArgument:
        raise
    
    # print("current session client is : " + str(session_client))
    # print("current session is:  " + str(session))
    response2 = MessageToDict(response._pb)
    param = response2['queryResult']['parameters']
    print(param)
    
    # ob = sendMessage(mobnum, sessionId)
    print("Query text:", response.query_result.query_text) # the text we just sent to the dialogflow
    # print("key nad value of variable ", response.query_result.parameters.fields.key)
    print("Detected intent:", response.query_result.intent.display_name) # intent which it belongs to
    print("Detected intent confidence: ", response.query_result.intent_detection_confidence) #confidence
    print("fulfillment text:", response.query_result.fulfillment_text) # the response

    

    intent_name = response.query_result.intent.display_name
   
    res = response.query_result.fulfillment_text
    if(intent_name == ''):
        ob = sendMessage(mobnum,sessionId)
        ob.text(res)
    
    # check = res.split()
    # print(check)
    # if check[0].lower() == 'enter' and check[-1].lower() == 'station.':
    #     print("inside this")
    #     flag = True 
    type = intent_name.split('_')[0]
    print(type)
    o = generate_type(res,sessionId,mobnum,intent_name,param)
    #temporary
    o.locations('Dehradun','Adventure')
    return 'trying'
    o.find(type)
   
    return response.query_result. fulfillment_text

    
def possible_list(value):
        # if(intent_name.split('_')[1] == 'train'):
            train_list(value)
    
def train_list(city,sId,num):
    l = []
    with open('data.csv','r') as file:
        read = csv.reader(file)
        # b1,b2 = False,False
        next(read)
        for r in read:
            f = city.replace(" ","").upper()
            if(f in r[1]):
                l.append(r[0])
                l.append(r[1])
    print("possible cities", l)
    msg = "Select the appropriate city from the list below."
    heading = "Select Station"
    custom_list(msg, heading,l,sId,num)

def custom_list(msg,heading,l,sId,num):
    opt = []
    for i in range(0,min(10,len(l)),2):
        d = {"tag" : l[i], "title" : l[i]}
        opt.append(d)
    ob  = sendMessage(num,sId)
    ob.lists(msg,heading, opt)

if  __name__ == '__main__':
    # home()
    app.run()    