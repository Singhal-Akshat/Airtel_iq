import requests
class sendMessage():

    url = "https://iqwhatsapp.airtel.in/gateway/airtel-xchange/basic/whatsapp-manager/v1/session/send/"
    headers = {
        'Authorization': 'Basic QUlSVEVMX0RJR192T0VsQUZxc0o4OVZoOXdxUVd4TDp6KkxVNktOPGt6c0w/K2JXMQ=='
    }
    bot_num = "918904584255"

    def __init__(self,mob, sId):
        self.sessionId = sId
        self.mobnum = mob
        
    def text(self,msg):
        curr_url = self.url + 'text'

        payload = {
            "sessionId" : self.sessionId,
            "to" : self.mobnum,
            "from" : self.bot_num,
            "message" : {
                "text" : msg
            }
        }
        self.send(curr_url, payload)

    def media(self,type,caption,url):
        curr_url = self.url + 'media'
        payload = {
            "sessionId" : self.sessionId,
            "to" : self.mobnum,
            "from" : self.bot_num,
            "mediaAttachment" :
            {
                "type" : type,
                "url" : url,
                "caption" : caption
            }
        }
        self.send(curr_url, payload)

    def buttons(self, msg, type, url, buttons):
       curr_url = self.url + 'interactive/buttons'

       if type=='':
        payload = {
            "sessionId" : self.sessionId,
            "to" : self.mobnum,
            "from" : self.bot_num,
            "message" : { "text" : msg},
            "buttons" : buttons
            }
       else : 
        payload = {
                "sessionId" : self.sessionId,
                "to" : self.mobnum,
                "from" : self.bot_num,
                "message" : { "text" : msg},
                "mediaAttachment" :  {
                    "type" : type,
                    "url" : url
                },
                "buttons" : buttons
        }

       self.send(curr_url, payload)

    def lists(self, msg,heading, options):
        curr_url = self.url + 'interactive/list'

        payload = {
            "sessionId" : self.sessionId,
            "to" : self.mobnum,
            "from" : self.bot_num,
            "message" :
            {
                "text" : msg
            },
            "list" : {
                "heading" : heading,
                "options" : options
            }
            
        }

        self.send(curr_url,payload)
    
    def template(self,tid,variable,url):
        curr_url = "https://iqwhatsapp.airtel.in/gateway/airtel-xchange/basic/whatsapp-manager/v1/template/send"
        payload = {
        "templateId": tid,
        "to": self.mobnum,
        "from": self.bot_num,
        "message": {
            "variables": variable,
            "suffix": url
        }
        }
        self.send(curr_url,payload)

    def template_media(self,tid,variable,type,aurl,url):
        curr_url = "https://iqwhatsapp.airtel.in/gateway/airtel-xchange/basic/whatsapp-manager/v1/template/send"
        payload = {
        "templateId": tid,
        "to": self.mobnum,
        "from": self.bot_num,
        "message": {
            "variables": variable,
            "suffix": url
        },
        "mediaAttachment" : {
            "type" : type,
            "url" : aurl
        }
        }
        self.send(curr_url,payload)
    def send(self, url, payload):
        response = requests.request("POST", url, headers= self.headers, json=payload)
        print(response.text.encode('utf-8'))

        