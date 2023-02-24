#!/user/bin/env/ python
import requests
import traceback
import datetime
import time
import json
from pprint import pprint

APIKEY="dc37139a1f5e7dbb1220eb237bc420120b3381f4"
NAME="Dublin"
STATIONS_URL="https://api.jcdecaux.com/vls/v1/stations" 


# def write_to_file(text):
#     with open("data/bikes_{}".format(now).replace(" ","_"),"w") as f:
#         f.write(r.text)

# def write_to_db(text):

def main():
#     run forever
    while True:
        try:
            now = datetime.datetime.now()
            r=requests.get(STATIONS_URL,params={"apiKey":APIKEY,"contract":NAME})
            # store(json.loads(r.text))
            # print(r.now)
            # write_to_file(r.text)
            # write_to_db(r.text)
            # now sleep for 5 minutes
            time.sleep(5*60)
            pprint(json.loads(r.text))
            
        except:
            # import traceback
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)
            print(traceback.format_exc())
        #     print("Failed")
    return

if __name__=="__main__":
    main()

