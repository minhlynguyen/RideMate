import sqlalchemy as sqla
import traceback
import datetime
import time
import requests
import json
from pprint import pprint
from sqlalchemy import create_engine
import glob
import os
from pprint import pprint
import simplejson as json
import requests
from IPython.display import display


# Getting station data using Station API
APIKEY="dc37139a1f5e7dbb1220eb237bc420120b3381f4"
NAME="Dublin"
STATIONS_URL="https://api.jcdecaux.com/vls/v1/stations" 

r=requests.get(STATIONS_URL,params={"apiKey":APIKEY,"contract":NAME})
stations=json.loads(r.text)

# Connect to RDS
URI = "dbbikes.c06rsktpo8sk.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "minhly"
PASSWORD = "22201371"
engine = create_engine("mysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)


# From station position getting the weather information there

# Creating a dictionary of station and its weather data: Station number is the key, weather data is the value

weather_station = {}

WEATHER_URL="https://api.open-meteo.com/v1/forecast"
HOURLY="temperature_2m","precipitation_probability","weathercode","windspeed_10m"

WEATHER_URL="https://api.open-meteo.com/v1/forecast"
HOURLY="temperature_2m","precipitation_probability","weathercode","windspeed_10m"
TIMEZONE="Europe/London"
DAILY="weathercode","temperature_2m_max","temperature_2m_min"
weather_station = {}

for station in stations:
    LATITUDE = station['position']['lat']
    LONGITUDE = station['position']['lng']
    weather=requests.get(WEATHER_URL,params={"latitude":LATITUDE,"longitude":LONGITUDE,"hourly":HOURLY,
    "daily":DAILY,"current_weather":"true","timeformat":"unixtime","timezone":TIMEZONE})
    weather_dict=json.loads(weather.text)
    weather_station[station['number']]=weather_dict

def weather_to_db():
    for station in weather_station:
        
         # Getting current weather data once every hour: 
        last_update = weather_station.get(station).get('current_weather').get('time')
        temperature = weather_station.get(station).get('current_weather').get('temperature')
        weathercode = weather_station.get(station).get('current_weather').get('weathercode')
        windspeed = weather_station.get(station).get('current_weather').get('windspeed')

        # Getting hourly weather forecast data for the next 12 hours only:
        hourly_time_full = weather_station.get(station).get('hourly').get('time')
        hourly_time = []
        hourly_temp = []
        hourly_preci = []
        hourly_weathercode = []
        hourly_windspeed = []
        i = hourly_time_full.index(last_update)

        for j in range(i,i+12):
            hourly_time.append(hourly_full[j])
            hourly_temp.append(weather_station.get(station).get('hourly').get('temperature_2m')[j])
            hourly_preci.append(weather_station.get(station).get('hourly').get('precipitation_probability')[j])
            hourly_weathercode.append(weather_station.get(station).get('hourly').get('weathercode')[j])
            hourly_windspeed.append(weather_station.get(station).get('hourly').get('windspeed_10m')[j])
        
        # Geting weather forecast data for 7 days
        daily_time = weather_station.get(station).get('daily').get('time')
        daily_weathercode = weather_station.get(station).get('daily').get('weathercode')
        daily_temp_max=weather_station.get(station).get('daily').get('temperature_2m_max')
        daily_temp_min=weather_station.get(station).get('daily').get('temperature_2m_min')
        
        # Insert weather data to table "weather"        
        val = (station, last_update, temperature, weathercode, windspeed, 
        str(hourly_time), str(hourly_temp), str(hourly_preci), str(hourly_weathercode), str(hourly_windspeed),
        str(daily_time),str(daily_weathercode),str(daily_temp_max),str(daily_temp_min))
        engine.execute("insert into weather values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",val)
        break
    return

weather_to_db()

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

