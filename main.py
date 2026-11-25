import requests

#fetching coordinates
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

#fetching apparent temperature and rain probability
params = {
    "latitude" : latitude,
    "longitude" : longitude,
    "hourly" : ["apparent_temperature", "precipitation_probability"],
    "forecast_days" : 1,
}   
response = requests.get("https://api.open-meteo.com/v1/forecast", params = params)
data = response.json()
forecast_temp = data["hourly"]["apparent_temperature"]
precipitation_probability = data["hourly"]["precipitation_probability"]







