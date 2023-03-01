# import statinAPI
def stations_to_db(text):
    stations=json.loads(text)
    print(type(stations),len(stations))

    for station in stations:
        print(station)
        # vals=(station.get('address'),int(station.get('banking')),station.get('available_bike_stands',int(station.get('bonus')),station.get('contract_name'),station.get('name'),get('contract_name'),station.get('number'),station.get('position').get('lat'),station.get('position').get('lng'),station.get('status'))
        break
    return

stations_to_db(r.text)