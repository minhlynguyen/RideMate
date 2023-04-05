#!/user/bin/env/ python
# import sqlalchemy
import datetime
import json
import threading
import time
import traceback
from pprint import pprint

import requests
import simplejson as json
import sqlalchemy as sqla
from sqlalchemy import create_engine, text

import config

try:
    engine = create_engine(
        "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)
except:
    engine = create_engine(
        "mysql://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)


def write_to_file(now, text):
    # the folder data in the same directory of this py code
    filename = "data/bikes/bikes_{}".format(
        now).replace(" ", "_").replace(":", "-")
    # now = datetime.datetime.now()
    with open(filename, "w") as f:
        f.write(text)


def stations_to_db(text):
    stations = json.loads(text)
    for station in stations:
        # db_update = int(time.time())
        # last_update = int(station.get('last_update')/1000)
        vals = (station.get('number'), station.get('address'), int(station.get('banking')),
                station.get('bike_stands'), int(station.get('bonus')),
                station.get('contract_name'), station.get('name'),
                station.get('position').get('lat'),
                station.get('position').get('lng'), station.get('status'), station.get('number'))
        engine.execute("""insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       ON DUPLICATE KEY UPDATE
                       number=%s
                       """, vals)
    return


def stations_availability_to_db(text):
    r = requests.get(config.STATIONS_URL, params={
                     "apiKey": config.APIKEY, "contract": config.NAME})

    # while True:
    stations = json.loads(text)
    for station in stations:
        last_update = int(station.get('last_update')/1000)
        vals = (station.get('number'), station.get('available_bikes'),
                station.get('available_bike_stands'),
                last_update, station.get('status'), station.get('number'), last_update)
        engine.execute("""insert into availability values(%s,%s,%s,%s,%s)
                       ON DUPLICATE KEY UPDATE
                       number=%s,
                       last_update=%s
                       """, vals)
    return


def weather_to_db(text):
    stations = json.loads(text)
    weather_station = {}
    for station in stations:
        LATITUDE = station['position']['lat']
        LONGITUDE = station['position']['lng']
        weather_request = requests.get(config.WEATHER_URL, params={"latitude": LATITUDE, "longitude": LONGITUDE, "hourly": config.HOURLY,
                                                                   "daily": config.DAILY, "current_weather": "true", "timeformat": "unixtime", "timezone": config.TIMEZONE})
        weather_dict = json.loads(weather_request.text)
        weather_station[station['number']] = weather_dict
#     print(weather_dict)

    # Insert current weather data to database:
    for station in weather_station:
        last_update = weather_station.get(
            station).get('current_weather').get('time')
        temperature = weather_station.get(station).get(
            'current_weather').get('temperature')
        weathercode = weather_station.get(station).get(
            'current_weather').get('weathercode')
        windspeed = weather_station.get(station).get(
            'current_weather').get('windspeed')
        vals_current = (station, last_update, temperature,
                        weathercode, windspeed, station, last_update)
        engine.execute("""insert into weather_current values(%s,%s,%s,%s,%s)
                       ON DUPLICATE KEY UPDATE
                       station=%s,
                       last_update=%s""", vals_current)
    return


def every_five_min():
    while True:
        # Scrape the station static data everyday, update the duplicate rows in database
        try:
            r = requests.get(config.STATIONS_URL, params={
                             "apiKey": config.APIKEY, "contract": config.NAME})
            stations_availability_to_db(r.text)
        # Stop for 5 minute
            time.sleep(5*60)
        except:
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)
            print(traceback.format_exc())
    return


def every_hour():
    while True:
        try:
            r = requests.get(config.STATIONS_URL, params={
                             "apiKey": config.APIKEY, "contract": config.NAME})
            weather_to_db(r.text)
            # Stop for 60 minutes
            time.sleep(60*60)
        except:
            # if there is any problem, print the traceback
            print(traceback.format_exc())
    return


def every_day():
    while True:
        try:
            r = requests.get(config.STATIONS_URL, params={
                             "apiKey": config.APIKEY, "contract": config.NAME})
            stations_to_db(r.text)
            # stop for 1 day
            time.sleep(24*60*60)
        except:
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)
            print(traceback.format_exc())
    return


def main():
    thread1 = threading.Thread(target=every_five_min)
    thread1.start()

    thread2 = threading.Thread(target=every_hour)
    thread2.start()

    thread3 = threading.Thread(target=every_day)
    thread3.start()


if __name__ == "__main__":
    main()
