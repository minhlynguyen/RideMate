import time
import requests
import json
from pprint import pprint

WEATHER_URL="https://api.open-meteo.com/v1/forecast"
LATITUDE = 53.31
LONGITUDE = -6.22

weather=requests.get(WEATHER_URL,params={"latitude":LATITUDE,"longitude":LONGITUDE,"hourly":"temperature_2m","hourly":"precipitation_probability","hourly":"precipitation","hourly":"weathercode","hourly":"windspeed_10m","current_weather":"true","timeformat":"unixtime"})
weather_dict=json.loads(weather.text)
pprint(json.loads(weather.text))

