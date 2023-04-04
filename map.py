import googlemaps
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # Set up the Google Maps client
    api_key = "AIzaSyC52j5KuFhqFUz3qfPc7s16bmfqRLb9wy8"
    gmaps = googlemaps.Client(api_key)

    # Search for a location in Dublin
    address = "Dublin, Ireland"
    geocode_result = gmaps.geocode(address)

    # Get the latitude and longitude of the location
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lng = geocode_result[0]["geometry"]["location"]["lng"]

    # Set up the map options
    map_options = {
        "center": {"lat": lat, "lng": lng},
        "zoom": 15
    }

    # Render the template with the map options and API key
    return render_template("map.html", map_options=map_options, api_key=api_key)


if __name__ == '__main__':
    app.run(debug=True)
