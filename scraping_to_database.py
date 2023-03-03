#!/user/bin/env/ python
# import sqlalchemy
import config
from sqlalchemy import create_engine, text
import sqlalchemy as sqla
import requests
import traceback
import datetime
import datetime
import time
import json
from pprint import pprint
from threading import Thread
import multiprocessing

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)

def write_to_file(now,text):
    
    # the folder data in the same directory of this py code
    filename="data/bikes/bikes_{}".format(now).replace(" ","_").replace(":", "-")
    # now = datetime.datetime.now()
    with open(filename,"w") as f:
        f.write(text)

def stations_to_db(text):
    # r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
    
    stations=json.loads(text)
    print(type(stations),len(stations))

    for station in stations:
        print(station)
        vals=(station.get('number'),station.get('address'),int(station.get('banking')),station.get('bike_stands'),int(station.get('bonus')),station.get('contract_name'),station.get('name'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'),station.get('number'))
        with engine.connect() as conn:
            # ups=mysql.insert(availability).values(vals)
            # ups=ups.on_duplicate_key_update
            conn.execute("""insert into station
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            number=%s
            """,vals)
            # conn.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
        break    
    # now sleep for 24 hours
    # time.sleep(5*60)
    return


def stations_availability_to_db(text):
    r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
    
    # while True:
    stations=json.loads(text)
    print(type(stations),len(stations))
    
    for station in stations:
        print(station)
        # vals=(station.get('number'),station.get('available_bikes'),station.get('available_bike_stands'),station.get('last_update'),station.get('status'))

        vals=(station.get('number'),station.get('available_bikes'),station.get('available_bike_stands'),station.get('last_update'),station.get('status'),station.get('number'),station.get('last_update'))
        with engine.connect() as conn:
            conn.execute("""insert into availability 
            values(%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            number=%s,
            last_update=%s
            """,vals)
        break
        # now sleep for 5 minutes
    # time.sleep(5*60)  
    # return

# From station position getting the weather information there
# Creating a dictionary of station and its weather data: Station number is the key, weather data is the value


def weather_to_db(text):
    # r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
    stations=json.loads(text)
    weather_station = {}
    for station in stations:
        LATITUDE = station['position']['lat']
        LONGITUDE = station['position']['lng']
        weather=requests.get(config.WEATHER_URL,params={"latitude":LATITUDE,"longitude":LONGITUDE,"hourly":config.HOURLY,
        "daily":config.DAILY,"current_weather":"true","timeformat":"unixtime","timezone":config.TIMEZONE})
        weather_dict=json.loads(weather.text)
        weather_station[station['number']]=weather_dict

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

        for j in range(i,i+24):
            hourly_time.append(hourly_time_full[j])
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
        str(daily_time),str(daily_weathercode),str(daily_temp_max),str(daily_temp_min),station, last_update)
        with engine.connect() as conn:
            conn.execute("""insert into weather values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
            station=%s,
            last_update=%s            
            """,val)     
        break
    # now sleep for one hour
    # time.sleep(5*60)  
    return

def every(delay,task):
    while True:
        time.sleep(delay)
        try:
            task
        except Exception:
            traceback.print_exc()






def main():
    r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})        
    # p1=multiprocessing.Process(target=stations_availability_to_db(r.text))
    # p1.start()
    # threading.Thread(target=lambda: every(5,stations_availability_to_db(r.text))).start()
    # run forever
    while True:
    #     # Scrape the station static data everyday, update the duplicate rows in database
        try:
            r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
            # stations_to_db(r.text)
            # p1=multiprocessing.Process(target=stations_availability_to_db())
            # p2=multiprocessing.Process(target=weather_to_db())
            # p3=multiprocessing.Process(target=stations_to_db())
            
            # p1.start()
            # p2.start()
            # p3.start()
            # threads=[Thread(target=stations_availability_to_db()),Thread(target=weather_to_db())]
            
            # for thread in threads:
            #     thread.start()
    
            # Thread(target=stations_to_db(r.text)).start()
            # Thread(target=stations_availability_to_db(r.text)).start()
            # Thread(target=weather_to_db(r.text)).start()
            # stations_to_db(r.text)
            # stations_availability_to_db(r.text)
            weather_to_db(r.text)
            time.sleep(5*60) 
    #         # Scrape the station static data everyday, update the duplicate rows in database            # now sleep for 24 hours
    #         # time.sleep(60*60*24)           
        except:
    #         # if there is any problem, print the traceback
            print(traceback.format_exc())

        # # Scrape the station analability dynamic data every 5 mins, insert rows in database
        # try:
        #     r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
        #     stations_availability_to_db(r.text)
        #     pprint(json.loads(r.text))
        #     # now sleep for 5 minutes
        #     time.sleep(5*60)           
        # except:
        #     # if there is any problem, print the traceback
        #     print(traceback.format_exc())
            
        # # # Scrape the weather dynamic data every one hour, insert rows in database
        # # try:
        # #     r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
        # #     # now sleep for one hour
        # #     time.sleep(60*60)           
        # # except:
        # #     # if there is any problem, print the traceback
        # #     print(traceback.format_exc())


if __name__ == "__main__":
    main()