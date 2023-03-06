#!/user/bin/env/ python
# import sqlalchemy
import config
from sqlalchemy import create_engine, text
import sqlalchemy as sqla
import requests
import traceback
import datetime
import time
import json
from pprint import pprint

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)

def write_to_file(now,text):
    # the folder data in the same directory of this py code
    filename="data/bikes/bikes_{}".format(now).replace(" ","_").replace(":", "-")
    # now = datetime.datetime.now()
    with open(filename,"w") as f:
        f.write(text)

def stations_to_db(text):
    stations=json.loads(text)
    print(type(stations),len(stations))

    for station in stations:
        print(station)
        vals=(station.get('address'),int(station.get('banking')),station.get('bike_stands'),int(station.get('bonus')),station.get('contract_name'),station.get('name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'),station.get('last_update'))
        with engine.connect() as conn:
            conn.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",vals)
        # break
    return


def stations_availability_to_db(text):
    stations=json.loads(text)
    print(type(stations),len(stations))
    
    for station in stations:
        print(station)
        vals=(station.get('number'),station.get('available_bikes'),station.get('available_bike_stands'),station.get('last_update'),station.get('status'))
        with engine.connect() as conn:
            conn.execute("insert into availability values(%s,%s,%s,%s,%s)",vals)
        # break
    return


def weather_to_db(text):
    stations = json.loads(text)
    weather_station = {}
    for station in stations:
        LATITUDE = station['position']['lat']
        LONGITUDE = station['position']['lng']
        weather_request=requests.get(config.WEATHER_URL,params={"latitude":LATITUDE,"longitude":LONGITUDE,"hourly":config.HOURLY,
        "daily":config.DAILY,"current_weather":"true","timeformat":"unixtime","timezone":config.TIMEZONE})
        weather_dict=json.loads(weather_request.text)
        weather_station[station['number']]=weather_dict
    print(weather_dict)
    
    # Insert current weather data to database: 
    for station in weather_station:
        last_update = weather_station.get(station).get('current_weather').get('time')
        temperature = weather_station.get(station).get('current_weather').get('temperature')
        weathercode = weather_station.get(station).get('current_weather').get('weathercode')
        windspeed = weather_station.get(station).get('current_weather').get('windspeed')        
        vals_current = (station, last_update, temperature, weathercode, windspeed)
        engine.execute("insert into weather_current values(%s,%s,%s,%s,%s)",vals_current)
        
        # Insert weather forecast data for next 24h for each station:        
        for i in range(0,24):
            forecast_time = weather_station.get(station).get('hourly').get('time')[i]
            temperature = weather_station.get(station).get('hourly').get('temperature_2m')[i]
            precipitation = weather_station.get(station).get('hourly').get('precipitation_probability')[i]
            weathercode = weather_station.get(station).get('hourly').get('weathercode')[i]
            windspeed = weather_station.get(station).get('hourly').get('windspeed_10m')[i]
            vals_hourly = (station, last_update, forecast_time, temperature, precipitation, weathercode, windspeed)
            engine.execute("insert into weather_forecast_24h values(%s,%s,%s,%s,%s,%s,%s)",vals_hourly)
    
        # Insert weather forecast data for next 7 days for each station:
        for j in range(0,7):
            last_update = weather_station.get(station).get('current_weather').get('time')
            forecast_day = weather_station.get(station).get('daily').get('time')[j]
            weathercode = weather_station.get(station).get('daily').get('weathercode')[j]
            temperature_max = weather_station.get(station).get('daily').get('temperature_2m_max')[j]
            temperature_min = weather_station.get(station).get('daily').get('temperature_2m_min')[j]
            vals_daily = (station, last_update, forecast_day, weathercode, temperature_max, temperature_min)
            engine.execute("insert into weather_forecast_7d values(%s,%s,%s,%s,%s,%s)",vals_daily)
#         break
    return

def main():
    # run forever
    while True:
        try:
            now = datetime.datetime.now()
            r=requests.get(config.STATIONS_URL,params={"apiKey":config.APIKEY,"contract":config.NAME})
            # store(json.loads(r.text))
            # print(r,now)
            # write_to_file(now,r.text)
            stations_to_db(r.text)
            stations_availability_to_db(r.text)
            pprint(json.loads(r.text))
            weather_to_db(r.text)
            # now sleep for 5 minutes
            time.sleep(5*60*12)
            # r.encoding='utf-8'
            # pprint(json.loads(r.text))
            

        except:
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)print(traceback.format_exc())
    return


if __name__ == "__main__":
    main()