#https://apidojo.github.io/#hotels-list
#https://rapidapi.com/apidojo/api/travel-advisor - attractions 
import requests
import json
#can be used to find hotels
#we are using it to find the location id of place 
# url = "https://travel-advisor.p.rapidapi.com/locations/search"

# querystring = {"query":"Dehradun","limit":"10","units":"km","currency":"INR","sort":"relevance","lang":"en_IN"}

# headers = {
# 	"X-RapidAPI-Key": "06f8a291fdmsh9e90c754007638fp128670jsnba3d71eb4a52",
# 	"X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring)

# ob = response.json()
# print(ob['data'][0]['result_object']['name'])
# print(ob['data'][0]['result_object']['location_id'])
# print(ob['data'][0]['result_object']['latitude'])
# print(ob['data'][0]['result_object']['longitude'])

def travelLocations():
	url = "https://travel-advisor.p.rapidapi.com/attractions/list"

	querystring = {"location_id":"297687","currency":"INR","lang":"en_IN","lunit":"km","sort":"recommended","limit" : 10}

	headers = {
		"X-RapidAPI-Key": "06f8a291fdmsh9e90c754007638fp128670jsnba3d71eb4a52",
		"X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	ob2 = response.json()

	print(ob2['data'][0]['name'])
	print(ob2['data'][0]['latitude'])
	print(ob2['data'][0]['longitude'])
	print(ob2['data'][0]['photo']['images']['original']['url'])
	print(ob2['data'][0]['description'])

#photo
# Name in bolds
# description
# timings: 
# google map link 

# asdfghjklasdfghjkl