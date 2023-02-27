#!/user/bin/env/ python
import sqlalchemy as sqla
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


metadata = sqla.MetaData()


def write_to_file(now,text):
    # the folder data in the same directory of this py code
    filename="data/bikes/bikes_{}".format(now).replace(" ","_").replace(":", "-")
    # now = datetime.datetime.now()
    with open(filename,"w") as f:
        f.write(text)

def write_to_db(text):
    stations=json.loads(text)
    print(type(stations),len(stations))

    for station in stations:
        print(station)
        vals=(station.get('address'),int(station.get('banking')),station.get('available_bike_stands',int(station.get('bonus')),station.get('contract_name'),station.get('name'),get('contract_name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status')),engine.execute("insert into station values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",vals))
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
            write_to_file(now,r.text)
            # write_to_db(r.text)
            # now sleep for 5 minutes
            time.sleep(5*60)
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



# metadata=sqla.MetaData()
# station = sqla.Table("station", metadata,
#     sqla.Column('address', sqla.String(256), nullable=False),
#     sqla.Column('banking', sqla.Integer),
#     sqla.Column('bike_stands', sqla.Integer),
#     sqla.Column('bonus', sqla.Integer),
#     sqla.Column('contrasct_name', sqla.String(256)),
#     sqla.Column('name', sqla.String(256)),
#     sqla.Column('number', sqla.Integer),
#     sqla.Column('position_lat', sqla.REAL),
#     sqla.Column('position_lng', sqla.REAL),
#     sqla.Column('status', sqla.BigInteger)
# )

# availability = sqla.Table("availability", metadata,
#     sqla.Column('available_bikes', sqla.Integer),
#     sqla.Column('available_bike_stands', sqla.Integer),
#     sqla.Column('number', sqla.Integer),
#     sqla.Column('last_update', sqla.Integer),
# )
# try:
#     station.drop(engine)
#     availability.drop(engine)
# except:
#     pass

# metadata.creat_all(engine)


# def stations_fix_keys(stations):
#     station['position_lat']=station['position']['lat']
#     station['position_lng']=station['position']['lng']
#     return station

# stations=json.loads(open('stations.json','r').read())

# engine.execute(station.insert(),*map(availability_fix_keys, stations))