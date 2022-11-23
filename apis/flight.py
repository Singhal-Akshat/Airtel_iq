
import requests
 
# Making a GET request
r = requests.get('https://www.google.com/q?=how+to+find+request')
 
# check status code for response received
# success code - 200
print("Here")
print(r)
 
# print content of request
print(r.content)