import requests


class GenerateHotels:

    headers = {
            "X-RapidAPI-Key": "06f8a291fdmsh9e90c754007638fp128670jsnba3d71eb4a52",
            "X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"}

    preference = {'Best Seller': 'PRICE_RELEVANT','Lowest Price': 'PRICE_LOW_TO_HIGH', 'Recommended' : 'RECOMMENDED' ,'Highest Rating':'REVIEW'}

    def GetDetails(self, city,start_date, end_date,pref):
        print('Get Details')
        info = []
        region_id = self.getDestinationId(city)

        url = "https://hotels-com-provider.p.rapidapi.com/v2/hotels/search"
        querystring = {"checkin_date": start_date, "checkout_date": end_date,
                       "sort_order": self.preference[pref], "region_id": region_id,
                       "adults_number": "1",
                       "locale": "en_IN", "domain": "IN"}
    
        response_hotel = requests.request("GET", url, headers=self.headers, params=querystring).json()
        count = 0
        # print(response_hotel)
        for i in response_hotel['properties']:
            hotel_name = i['name']
            hotel_price = i['price']['lead']['formatted']
            hotel_supplier_id = i['id']
            hotel_ratings = i['reviews']['score']/2
            lat = i['mapMarker']['latLong']['latitude']
            long = i['mapMarker']['latLong']['longitude']
            hotel_address = self.getAddress(lat,long)
            map = hotel_name.replace(" ",'+')
            map = map.replace(",","%2C")
            hotel_image = self.getImage(map)
            if(hotel_image == ''):
                continue
            map_url = "https://www.google.com/maps/search/?api=1&query="+map+"+"+city
            hotel_booking_url = "https://in.hotels.com/Hotel-Search?destination="+map+"&selected="+str(hotel_supplier_id)+"&startDate="+start_date+"&endDate="+end_date

            temp = [hotel_name, hotel_price, hotel_ratings,hotel_address, hotel_image,map_url,hotel_booking_url]
            info.append(temp)
            count+=1
            if(count==6):
                break
        print("Size :", len(info))
        return info[:6]
    
    def getAddress(self,lat,long):
        key = "AIzaSyCTvLmX7b6eQKf3JqYLSVKeu7MqyM2Yar4"
        payload ={}
        headers ={}
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(lat)+","+str(long)+"&key="+key
        response = requests.request("GET",url, headers=headers, data=payload).json()
        address = response['results'][0]['formatted_address']
        # print(response['results'][0]['formatted_address'])
        return address
        

    def getImage(self,hotel):
        key = "AIzaSyCTvLmX7b6eQKf3JqYLSVKeu7MqyM2Yar4"
        payload ={}
        headers ={}
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+hotel+"&key="+key
        response = requests.request("GET",url, headers=headers, data=payload).json()
     
        for d in response['results']:
            try:
                img_ref = d['photos'][0]['photo_reference']
            except:
                print("inside this")
                return ''
        image_link = self.get_image(img_ref,key)
        return image_link
    def get_image(self,id,key):
        url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference="+id+"&key="+key
        return url
    def getDestinationId(self,city):
        print('Get Destination Id')
        url = "https://hotels-com-provider.p.rapidapi.com/v2/regions"
        querystring = {"locale":"en_IN","query":city,"domain":"IN"}
        response = requests.request("GET", url, headers=self.headers, params=querystring).json()
        # print(response)
        destination_id = response['data'][0]['gaiaId']
        return destination_id

    def GetPhotos(self, hotel_id):
        url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/photos"
        querystring = {"hotel_id": hotel_id}
        
        response_pics = requests.request("GET", url, headers=self.headers, params=querystring).json()
        get_pic = response_pics[0]['mainUrl']
        return get_pic

    def GetReviews(self, hotel_id):
        get_reviews = []
        url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/reviews"
        querystring = {"locale": "en_IN", "hotel_id": hotel_id, "page_number": "1"}

        review_response = requests.request("GET", url, headers=self.headers, params=querystring).json()


ob = GenerateHotels()
print(ob.GetDetails("Dehradun","2022-12-09","2022-12-10","Best Seller"))
