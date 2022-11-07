# instal : pip instal pyyaml
import json
import yaml
import os
dict = {}

def nlu():
    intent_name = json_object['name'] 

    list_intent = []
    print(json_object)
    for intent in json_object['userSays']:
        print(intent)
        list_intent.append(intent['data'][0]['text'])

    with open('intent.yaml','a') as file:
        yaml.dump({'intent' : intent_name},file)
        yaml.dump({'examples': list_intent},file)

def domain():
    intent_name = json_object['name'] 
    response = json_object['responses'][0]['messages'][0]['speech'][0]
    
    with open('response.yaml','a') as file:
        name = 'utter_' + intent_name
        yaml.dump({name: {'text' : response,'image' : 'sdfsd'}},file)

folder = 'test\intents'
for file in os.listdir(folder):
    path = os.path.join(folder,file)
    print(path)
    with open(path) as openfile:
        json_object = json.load(openfile)
    nlu()
    domain()

