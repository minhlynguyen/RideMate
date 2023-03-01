import sqlalchemy as sqla
import traceback
import datetime
import time
import requests
import json
from pprint import pprint

# Getting station data using Station API
APIKEY="dc37139a1f5e7dbb1220eb237bc420120b3381f4"
NAME="Dublin"
STATIONS_URL="https://api.jcdecaux.com/vls/v1/stations" 

r=requests.get(STATIONS_URL,params={"apiKey":APIKEY,"contract":NAME})
stations=json.loads(r.text)

# From station position getting the weather information there

# Creating a dictionary of station and its weather data: Station number is the key, weather data is the value

weather_station = {}

WEATHER_URL="https://api.open-meteo.com/v1/forecast"
HOURLY="temperature_2m","precipitation_probability","weathercode","windspeed_10m"

for station in stations:
    LATITUDE = station['position']['lat']
    LONGITUDE = station['position']['lng']
    weather=requests.get(WEATHER_URL,params={"latitude":LATITUDE,"longitude":LONGITUDE,"hourly":HOURLY,"current_weather":"true","timeformat":"unixtime"})
    weather_dict=json.loads(weather.text)
    weather_station[station['number']]=weather_dict

pprint(weather_station[42])

def write_to_file(now, text):
    now = datetime.datetime.now()
    filename = "data/weather_{}".format(now).replace(" ","_").replace(":", "-")
    with open(filename, "w") as f:
        f.write(text)


def write_to_db(text):
    weather_db = json.loads(text)
    for weather_rep in weather_db:
        print(weather_rep)
        break
    return


def main():
    while True:
        try:
            now = datetime.datetime.now()
            write_to_file(now, weather.text)
            write_to_db(weather.text)
            time.sleep(5*60)
            pprint(json.loads(weather.text))
        except:
            print(traceback.format_exc())

        return

