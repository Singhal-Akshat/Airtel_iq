# 30.270265, 77.992899
import requests
import json
class generate_locations():
    key = "AIzaSyCTvLmX7b6eQKf3JqYLSVKeu7MqyM2Yar4"
    payload ={}
    headers ={}
    types = {'Tourist Point' : ['tourist_attraction','point_of_interest'] ,'Amusement park' : ['amusement_park'],'Spiritual': ['hindu_temple','mosque','church'],'Museum and Art':['museum','art_gallery'],'Zoo and Aquarium':['aquarium','zoo'],'Night Club' :['night_club','bar'],'Casino':['casino'],'Stadium' : ['stadium']}
    def search(self,city,type):
        data = []
        city =city.replace(" ","%20")
        for t in self.types[type]:
            print(t)
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+city+"&type="+t+"&key="+self.key
            response = requests.request("GET",url, headers=self.headers, data=self.payload).json()
            # print(len(response['results']))
            # print(response['results'])
            for d in response['results']:
                try:
                    img_ref = d['photos'][0]['photo_reference']
                except:
                    print("inside this")
                    continue
                name = d['name']
                flag = False
                for n in data:
                    if name == n[1]:
                        flag = True
                        break
                if(flag):
                    continue
                lat = d['geometry']['location']['lat']
                long = d['geometry']['location']['lng']
                id = d['place_id']
                rating = d['rating']
                user_rating = d['user_ratings_total']
                types=""

                for t in d['types']:
                    if t=='point_of_interest' or t=='establishment':
                        continue
                    g = t.split('_')
                    for h in g:
                        types += h +' '
                    types =types[:-1]
                    types+=', '
                types = types[:-2]
                
                location_link = self.get_link(lat,long,id)
                image_link = self.get_image(img_ref)

                temp = [rating,name,types,image_link,location_link,user_rating]

                data.append(temp)
                # print(data)
        
        data.sort(reverse=True, key=self.myfunc)
        return data[:min(6,len(data))]
    def myfunc(self,e):
        return e[-1]
    def get_link(self,lat,long,id):
        # url = "https://www.google.com/maps/search/?api=1&query="+str(lat)+"%2C"+str(long)+"&query_place_id="+id
        url = "?api=1&query="+str(lat)+"%2C"+str(long)+"&query_place_id="+id
        return url
    
    def get_image(self,id):
        url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference="+id+"&key="+self.key
        return url