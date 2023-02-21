import requests
import json

NAME = "Dublin"
STATIONS="https://api.jcdecaux.com/vls/v1/stations"
APIKEY = "8c2695c52b410350a8b28f39666153b0185afc8f"
def main():
    while True:
        try:
            r = requests.get(STATIONS,params={"apiKey":APIKEY,"contract": NAME})
            
            store(json.loads(r.text))
            # query="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=8c2695c52b410350a8b28f39666153b0185afc8f"
            # r=requests.get(query)

            time.sleep(5*60)
print(json.loads(r.text))

# # print(getreq.json.())

# print(type(getreq))

