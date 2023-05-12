from send import sendMessage
from flask import Flask
import csv
from flask import  request
from google_apis import generate_locations
from hotel_api import GenerateHotels
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
        url =  self.mediaurl(con)
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
        url = self.mediaurl(con)
        if(url!=''):
            con = con[:-1]
        
        for i in range(2,min(5,len(con))):
            d = {"tag" : con[i], "title" : con[i]}
            but.append(d)
        
        self.ob.buttons(msg,type,url,but)
    
    def mediaurl(self,con):
        if con[0]!='':
            return con[-1]
        else:
            return ''

    def check_param(self):
        dict = self.parameters
        intent_name = self.intent_name.split('_')[1]
        if(len(dict)) :
            if ( intent_name == 'places'):
                if dict['city']!='':
                    if('type'  == self.response.lower()):
                        self.possible_list(dict['city'])
                        return True
                for key,value in self.parameters.items():
                    if value=="":
                        return False
            elif (intent_name == 'hotel'):
                if 'pref' == self.response.lower():
                    self.possible_list()
                    return True

                for key,value in dict.items():
                    if value=="":
                        return False
            else:
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
        intent = self.intent_name.split('_')[1].lower()
        dict = self.parameters
        

        if intent == 'train':
            variable = [dict['from'],dict['to'],dict['date'][:10]]
            url = "?from_code="+dict['from2']+"&journey_date="+dict['date'][:10]+"&to_code=" +dict['to2']
            image_url = "https://i.pinimg.com/736x/df/91/f5/df91f500c925e30391e72b941a4f42c3.jpg"
            self.ob.template_media("2d6e4f8a-912d-4d27-bbf8-3aceef012664",variable,"IMAGE",image_url,url)
            self.custom_button("Want to Book another ticket?","Yes,No")
        elif intent == 'flight':
            #https://www.makemytrip.com/flight/search?itinerary=DEL-PNQ-28/11/2022&tripType=O&paxType=A-4_C-0_I-0&cabinClass=E
            variable = [dict['from'],dict['to'],dict['date'][:10]]
            date = dict['date'][:10]
            year = date[:4]
            mon = date[5:7]
            day = date[8:10]
            print(day,mon,year,date)
            passenger = str(dict['Passengers']).split('.')[0]
            url = "search?itinerary="+dict['from2']+"-"+dict['to2']+"-"+day+"/"+mon+"/"+year+"&tripType=O&paxType=A-"+passenger+"_C-0_I-0&cabinClass=E"
            variable.append(passenger)
            image_url = "https://media.istockphoto.com/id/1130104432/vector/airport-building-exterior-with-buses-and-airplanes-vector-flat-style-illustration.jpg?b=1&s=612x612&w=0&k=20&c=AV49ZpW13how4iGPxz_7_vnbBv3GeuMiFqYA8ZCivmM="
            self.ob.template_media("dff006c2-6740-47c6-a43f-996b9e73e81c",variable,"IMAGE",image_url,url)
            self.custom_button("Want to Book another ticket?","Yes,No")
        
        elif intent == 'places':
            city = self.parameters['city']
            type = self.parameters['type']
            self.locations(city,type)
            self.custom_button("Want to see another place","See another place,No")
        elif intent == 'hotel':
            city = dict['city']
            start = dict['start'][:10]
            end = dict['end'][:10]
            pref = dict['pref']
            self.hotels(city,start,end,pref)
            self.custom_button("Want to search for hotels in another city?","Hotel Bookings,No")
        elif intent == 'bus':
            frm = dict['from']
            to = dict['to']
            date = dict['date'][:10]
            year = date[:4]
            mon = date[5:7]
            day = date[8:10]
            url = frm+"/"+to+"/"+day+"-"+mon+"-"+year
            variable = ["Bus",frm,to,date]
            image_url = "https://st.redbus.in/Images/India/ContextualLogin/generic_banner_Ind.png"
            self.ob.template_media("38a12480-553e-4a8f-b8c8-42a1b1b5b15e",variable,"IMAGE",image_url,url)
            self.custom_button("Want to Book another ticket?","Yes,No")
        return True

    def possible_list(self,value=''):
        intent = self.intent_name.split('_')[1].lower()
        print(intent)
        if(intent == 'train'):
            self.train_list(value)
        elif intent == 'flight':
            self.airport_list(value)
        elif intent == 'places':
            self.types_list(value)
        elif intent == 'hotel':
            self.preference_list()
    
    def types_list(self,value):
        l = ['Tourist Point','Amusement park','Spiritual','Museum and Art','Zoo and Aquariam','Night Club','Casino','Stadium']
        opt = []
        for i in range(0,min(10,len(l))):
            d = {"tag" : l[i], "title" : l[i]}
            opt.append(d)
        msg = "Select the types of places you want to see in *" + value + "* from the options below"
        heading = "Select Location Type"
        self.ob.lists(msg,heading, opt)

    def preference_list(self):
        l = ['Best Seller','Lowest Price', 'Recommended','Highest Rating']
        opt = []
        for i in range(0,len(l)):
            d = {"tag" : l[i], "title" : l[i]}
            opt.append(d)
        msg = "Select your preference :"
        heading = "Preference Options"
        self.ob.lists(msg,heading,opt)
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
        msg = "Select the appropriate airport from the list below"
        heading = "Select Airport"
        self.custom_list(msg,heading,l)

    def custom_list(self,msg,heading,l):
        opt = []
        for i in range(0,min(20,len(l)),2):
            d = {"tag" : l[i], "title" : l[i],"description" : l[i+1]}
            opt.append(d)
        self.ob.lists(msg,heading, opt)
    
    def custom_button(self,msg,b,type='',url=''):
        but = b.split(',')
        button =[]
        for i in range(len(but)):
            d = {"tag" : but[i], "title" : but[i]}
            button.append(d)

        self.ob.buttons(msg,type,url,button)

    def locations(self,city,type):
        ob = generate_locations()
        data = ob.search(city,type)
        if(len(data)==0):
            self.ob.text("No "+type+" available in "+city)
            return
        for d in data:
            # caption = "*Name:* "+ d[1]+ '\n\n'+ "*Types:* "+d[2] + '\n\n' + '*Rating:* ' + str(d[0]) + '⭐' + '\n\n' + '*Google Map:* '+d[4]
            caption =  d[1]+ '\n\n'+ "*Types:* "+d[2] + '\n\n' + '*Rating:* ' + str(d[0]) + '⭐'
            # self.ob.media("IMAGE",caption,d[3])
            self.ob.template_media('49ec73fa-379b-4869-8da7-bd5391dff752',[": "+d[1],": "+d[2],": " + str(d[0])+'⭐'],"IMAGE",d[3],d[4])

    def hotels(self,city,start,end,pref):
        ob = GenerateHotels()
        data = ob.GetDetails(city,start,end,pref)
        for d in data:
            refund = ""
            if(d[3]):
                refund = "yes"
            else:
                refund = "no"

            # caption = '*Name:* ' + d[0] + '\n\n*Price:* ' + d[1] + '\n\n*Ratings:* ' + str(d[2]) + '⭐' + '\n\n*Refundable:* ' + refund + '\n\n*Address:* ' + d[4]+'\n\n*Google Map:* ' + d[-2] + '\n\n*To Book:* ' + d[-1]
            caption = '*Name:* ' + d[0] + '\n\n*Price:* ' + d[1] + '\n\n*Ratings:* ' + str(d[2]) + '⭐' + '\n\n*Address:* ' + d[3]+'\n\n*Google Map:* ' + d[-2] + '\n\n*To Book:* ' + d[-1]
            self.ob.media("IMAGE",caption,d[-3])

  