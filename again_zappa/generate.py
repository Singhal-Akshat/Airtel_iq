from send import sendMessage
from flask import Flask
import csv
import requests
from flask import  request
from google_apis import generate_locations
class generate_type:
    
    def __init__(self,res,Sid, num, iname,p):
        self.response = res
        self.id = Sid
        self.num = num
        self.ob = sendMessage(num,Sid)
        self.intent_name = iname
        self.parameters = p

    def find(self,type):
        if(self.check_param()):
            return
        if type == 'text':
            self.ob.text(self.response)
        elif type == 'media':
            self.generate_media()
        elif type == 'list':
            self.generate_list()
        elif type == 'button':
            self.generate_button()
    
    def generate_media(self):
        con = self.response.split('#')
        type = con[0]
        caption = con[1]
        url = self.mediaurl()
        self.ob.media(type,caption,url)
    
    def generate_list(self):
        con = self.response.split('#')
        msg = con[0]
        heading = con[1]
        opt = []
        for i in range(2,len(con),2):
            d = { "tag" : con[i], "title" : con[i], "description" : con[i+1]}
            opt.append(d)
        
        self.ob.lists(msg,heading, opt)
    
    def generate_button(self):
        con = self.response.split('#')
        type = con[0]
        msg = con[1]
        but=[]
        url = self.mediaurl()
        for i in range(2,len(con)):
            d = {"tag" : con[i], "title" : con[i]}
            but.append(d)
        
        self.ob.buttons(msg,type,url,but)
    
    def mediaurl(self):
        return ""

    def check_param(self):
        dict = self.parameters
        if(len(dict)) :
            if dict['from']!='' or dict['to']!='': 
                if('boarding' == self.response.lower()):
                    print(dict['from'])
                    self.possible_list(dict['from'])
                    return True
                if('destination' == self.response.lower()):
                    print(dict['to'])
                    self.possible_list(dict['to'])
                    return True
            
            for key,value in self.parameters.items():
                if value=="":
                    return False
            
            return self.generate_links()

    def generate_links(self):
        transport = self.intent_name.split('_')[1].lower()
        dict = self.parameters
        variable = [dict['from'],dict['to'],dict['date'][:10]]

        if transport == 'train':
            url = "?from_code="+dict['from2']+"&journey_date="+dict['date'][:10]+"&to_code=" +dict['to2']
            self.ob.template("5ac1c243-a21d-43b7-97fc-da624c00df20",variable,url)
            
        elif transport == 'flight':
            date = dict['date'][:10]
            year = date[:4]
            mon = date[5:7]
            day = date[8:10]
            print(day,mon,year,date)
            passenger = str(dict['Passengers']).split('.')[0]
            url = "search?itinerary="+dict['from2']+"-"+dict['to2']+"-"+day+"/"+mon+"/"+year+"&tripType=O&paxType=A-"+passenger+"_C-0_I-0&cabinClass=E"
            variable.append(passenger)
            self.ob.template("46e838f2-8158-4702-b165-c1a125497169",variable,url)
        
        self.custom_button("Want to Book another ticket?","Yes,No",'','')
        return True

    def possible_list(self,value):
        transport = self.intent_name.split('_')[1].lower()
        print(transport)
        if(transport == 'train'):
            self.train_list(value)
        elif transport == 'flight':
            print(transport)
            self.airport_list(value)
    
    def train_list(self,city):
        l = []
        with open('data.csv','r') as file:
            read = csv.reader(file)
            next(read)
            for r in read:
                f = city.replace(" ","").upper()
                if(f in r[1]):
                    l.append(r[0])
                    l.append(r[1])
        msg = "Select the appropriate city from the list below."
        heading = "Select Station"
        self.custom_list(msg, heading,l)

    def airport_list(self,city):
        l = []
        f = city.replace(" ","").lower()
        with open('airport.csv','r') as file:
            read = csv.reader(file)
            next(read)
            for r in read:
                c = r[0].replace(" ","").lower()
                if(f in c):
                    l.append(r[2])
                    l.append(r[0])
        msg = "select the appropriate airport from the list below"
        heading = "select airport"
        self.custom_list(msg,heading,l)

    def custom_list(self,msg,heading,l):
        opt = []
        for i in range(0,min(20,len(l)),2):
            d = {"tag" : l[i], "title" : l[i],"description" : l[i+1]}
            opt.append(d)
        self.ob.lists(msg,heading, opt)
    
    def custom_button(self,msg,b,type,url):
        but = b.split(',')
        button =[]
        for i in range(len(but)):
            d = {"tag" : but[i], "title" : but[i]}
            button.append(d)

        self.ob.buttons(msg,type,url,button)

    def locations(self,city,type):
        ob = generate_locations()
        data = ob.search(city,type)

        for d in data:
            caption = "*Name:* "+ d[1]+ '\n\n'+ "*Types:* "+d[2] + '\n\n' + '*Rating:* ' + str(d[0]) + '⭐' + '\n\n' + '*Google Map:* '+d[4]
            self.ob.media("IMAGE",caption,d[3])
            # self.ob.template_media('',[d[1],d[2],str(d[0])],"IMAGE",d[3],d[4])


  