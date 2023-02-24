#!/user/bin/env/ python
import requests
import traceback
import datetime
import datetime
import time
import json
from pprint import pprint

APIKEY="dc37139a1f5e7dbb1220eb237bc420120b3381f4"
NAME="Dublin"
STATIONS_URL="https://api.jcdecaux.com/vls/v1/stations" 


def write_to_file(text):
    now = datetime.datetime.now()
    with open("data/bikes_{}".format(now).replace(" ","_"),"w") as f:
        f.write(r.text)

def write_to_db(text):
    stations=json.loads(text)
    print(type(stations),len(stations))

    for station in stations:
        print(station)
        # vals=(station.get('address'),int(station.get('banking')),station.get('available_bike_stands',int(station.get('bonus')),station.get('contract_name'),station.get('name'),get('contract_name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'))
        break
    return

def main():
    # run forever
    while True:
        try:
            now = datetime.datetime.now()
            r=requests.get(STATIONS_URL,params={"apiKey":APIKEY,"contract":NAME})
            # store(json.loads(r.text))
            # print(r,now)
            write_to_file(r.text)
            write_to_db(r.text)
            # now sleep for 5 minutes
            time.sleep(5)
            # r.encoding='utf-8'
            station=json.loads(r.text)
            # pprint(json.loads(r.text))
            pprint(station)
            # station_array=[]
            # for i in range(len(station)):
            #     station_array.append(station[i]['position'])
            # print(station_array)
            # positions=r.json()['position'][0]['lat']
            # pprint(positions)
            
        except:
            # import traceback
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)
            print(traceback.format_exc())
        #     print("Failed")
            # if engine is None:
    return

if __name__=="__main__":
    main()


# def stations_to_db(text):
#     stations=json.loads(text)
#     print(type(stations),len(stations))

#     for station in stations:
#         print(station)
#         # vals=(station.get('address'),int(station.get('banking')),station.get('available_bike_stands',int(station.get('bonus')),station.get('contract_name'),station.get('name'),get('contract_name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'))
#         break
#     return

# stations_to_db(r.text)