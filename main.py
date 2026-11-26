import requests
from desktop_notifier.sync import DesktopNotifierSync



def main():
    notifier = DesktopNotifierSync()


    #fetching coordinates
    lines = []
    THRESHOLD = 8 #threshold for jacket set to 8 degrees celsius
    jacket = False
    umbrella = False
    with open ("./location.txt", "r") as file:
        lines = file.read().strip().split("\n") #extracting lines from location file.

    #invalid location file format
    if (len(lines) != 2):
        with open ("./forecast.txt", "w") as f:
            f.write("location.txt must have two lines, first line must be location and second line must be timezone.")
            notifier.send(title = "Error", message = "location.txt must have two lines, first line must be location and second line must be timezone.")
        return 
    
    location = lines[0]
    timezone = lines[1]

    #parameters for open-meteo coordinates GET request
    params = {
        "name" : location,
        "count" : 1,
        "language": "en"
    } 

    response = requests.get("https://geocoding-api.open-meteo.com/v1/search", params = params)
    data = response.json()
    latitude = 0
    longitude = 0
    reason = ""

    #coordinates
    if "results" in data: #no errors if results key in data
        latitude = data["results"][0]["latitude"] 
        longitude = data["results"][0]["longitude"]
    elif "reason" in data:
        #API fetch error
        reason = data["reason"]
        with open ("./forecast.txt", "w") as f:
            f.write("error: " + reason)
            notifier.send(title = "Error", message = ("error: " + reason))
            return
    else:
        #location not found
        with open ("./forecast.txt", "w") as f:
            f.write("error: location not found")
            notifier.send(title = "Error", message = ("location not found"))
            return


        
    
    

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
    forecast_temp = []
    precipitation_probability = []

    if "hourly" in data: #no errors if results key in data
        forecast_temp = data["hourly"]["apparent_temperature"]
        precipitation_probability = data["hourly"]["precipitation_probability"]
    else:
        #API fetch error
        reason = data["reason"]
        with open ("./forecast.txt", "w") as f:
            f.write("error: " + reason)
            notifier.send(title = "Error", message = reason)
            return
        
    

    #jacket and umbrella recommendations
    for i in range(24, len(forecast_temp)):
        if (forecast_temp[i] <= THRESHOLD):
            jacket = True
        if (precipitation_probability[i] >= 50):
            umbrella = True
        if (jacket and umbrella): 
            break
    #add recommendations to forecast.txt file and send notifications
    with open ("./forecast.txt", "w") as f:
        if (jacket):
            f.write("Bring a jacket with you tomorrow\n")
            notifier.send(title = "Weather Alert", message = "Bring a jacket with you tomorrow")
        else:
            f.write("Do not bring a jacket\n")
            notifier.send(title = "Weather Alert", message = "Do not bring a jacket with you tomorrow")
        if (umbrella):
            f.write("Bring an umbrella with you\n")
            notifier.send(title = "Weather Alert", message = "Bring an umbrella with you tomorrow")
        else:
            f.write("Do not bring an umbrella with you\n")
            notifier.send(title = "Weather Alert", message = "Do not bring an umbrella with you")

        




main()




