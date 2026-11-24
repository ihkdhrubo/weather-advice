import requests

location = []
with open ("./location.txt", "r") as file:
    location = file.read().strip() #extracting location from file.

params = {
    "name" : location,
    "count" : 1,
    "language": "en"
} #params for get request

response = requests.get("https://geocoding-api.open-meteo.com/v1/search", params = params)
data = response.json()

#coordinates
latitude = data["results"][0]["latitude"] 
longitude = data["results"][0]["longitude"]



