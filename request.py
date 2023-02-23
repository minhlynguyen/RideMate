
import time
import requests
import json
from pprint import pprint

JCKEY="dc37139a1f5e7dbb1220eb237bc420120b3381f4"
NAME="dublin"
STATIONS_URL="https://api.jcdecaux.com/vls/v1/stations" 

# def main():
    # run forever
    # while True:
    #     try:
r=requests.get(STATIONS_URL,params={"apiKey":JCKEY,"contract":NAME})
            # store(json.loads(r.text))

            # now sleep for 5 minutes
            # time.sleep(5*60)
pprint(json.loads(r.text))
        # except:
            # import traceback
            # if there is any problem, print the traceback
            # traceback.print_exception(*exc_info)
            # print(traceback.format_exc())
            # print("Failed")
    # return


# r = requests.get(URI, params={'q':'bob', 'type':'artist', 'limit':2}) 
