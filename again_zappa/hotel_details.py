import requests
import json
#search_by_name to get destination id for a city serves no other purpose(probably)
url = "https://hotels-com-provider.p.rapidapi.com/v1/destinations/search"
#city name ie query to be extracted from user
querystring = {"query":"Dehradun","currency":"INR","locale":"en_IN"}

headers = {
	"X-RapidAPI-Key": "486895e200mshd19ceb91935b226p1f4118jsnb19ade0f6f43",
	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
objekt=response.json()
#gets destination_id
destination_id=objekt['suggestions'][0]['entities'][0]['destinationId']

#get hotels list: name-coordinates-rating-address ON BASIS OF destination_id


url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/search"
#check-in and out date to be extracted from user
querystring = {"checkin_date":"2023-01-26","checkout_date":"2023-01-27","sort_order":"STAR_RATING_HIGHEST_FIRST","destination_id":destination_id,"adults_number":"1","locale":"en_IN","currency":"INR"}

'''
sort_order options:

STAR_RATING_HIGHEST_FIRST
STAR_RATING_LOWEST_FIRST
BEST_SELLER
DISTANCE_FROM_LANDMARK
GUEST_RATING
PRICE_HIGHEST_FIRST
PRICE
'''

headers = {
	"X-RapidAPI-Key": "486895e200mshd19ceb91935b226p1f4118jsnb19ade0f6f43",
	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
}

response_hotel = requests.request("GET", url, headers=headers, params=querystring)

hotel_objekt=response_hotel.json()

#refundable returns boolean value

hotel_name= hotel_objekt['searchResults']['results'][1]['name']
hotel_id= hotel_objekt['searchResults']['results'][1]['id']
hotel_price=hotel_objekt['searchResults']['results'][1]['ratePlan']['price']['current']
hotel_coordinates=hotel_objekt['searchResults']['results'][1]['coordinate']
hotel_ratings=hotel_objekt['searchResults']['results'][1]['starRating']
hotel_refundable=hotel_objekt['searchResults']['results'][1]['ratePlan']['features']['freeCancellation']
hotel_address=hotel_objekt['searchResults']['results'][1]['address']['streetAddress']+","+hotel_objekt['searchResults']['results'][1]['address']['extendedAddress']+","+hotel_objekt['searchResults']['results'][1]['address']['locality']+","+hotel_objekt['searchResults']['results'][1]['address']['region']+","+hotel_objekt['searchResults']['results'][1]['address']['countryName']
print(hotel_name,hotel_id,hotel_price,hotel_coordinates,hotel_ratings,hotel_refundable,hotel_address)


#get hotel pics on basis of selected hotel?? because idk thats how it works


url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/photos"
#requires hotel_id which was extracted by get hotel lists
querystring = {"hotel_id":hotel_id}

headers = {
	"X-RapidAPI-Key": "486895e200mshd19ceb91935b226p1f4118jsnb19ade0f6f43",
	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
}

response_pics = requests.request("GET", url, headers=headers, params=querystring)

pics_objekt= response_pics.json()

get_pic= pics_objekt[0]['mainUrl']

print(get_pic)

#get reviews for hotel hehe boi

url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/reviews"
#requirement same as get_pic 
querystring = {"locale":"en_IN","hotel_id":hotel_id,"page_number":"1"}

headers = {
	"X-RapidAPI-Key": "486895e200mshd19ceb91935b226p1f4118jsnb19ade0f6f43",
	"X-RapidAPI-Host": "hotels-com-provider.p.rapidapi.com"
}

review_response = requests.request("GET", url, headers=headers, params=querystring)
review_objekt= review_response.json()
for i in range(0,10):
    get_reviews=str(i+1)+"\n"+review_objekt['groupReview'][0]['reviews'][i]['title']+"\n"+review_objekt['groupReview'][0]['reviews'][i]['summary']+"\n"
    print(get_reviews)


