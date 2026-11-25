import requests

#fetching coordinates
location = []
THRESHOLD = 8
jacket = False
with open ("./location.txt", "r") as file:
    location = file.read().strip() #extracting location from file.

timezone = location.split("\n")[1]
location = location.split("\n")[0]


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
    "forecast_days" : 2,
    "timezone" : timezone
}   
response = requests.get("https://api.open-meteo.com/v1/forecast", params = params)
data = response.json()
print(data)
forecast_temp = data["hourly"]["apparent_temperature"]
precipitation_probability = data["hourly"]["precipitation_probability"]

for i in range(24, len(forecast_temp)):
    if (forecast_temp[i] < THRESHOLD):
        jacket = True
        break
        









