import googlemaps
import mysql.connector
import mysql.connector.pooling
from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
api_key = "AIzaSyC52j5KuFhqFUz3qfPc7s16bmfqRLb9wy8"
GoogleMaps(app, key=api_key)

# Define the MySQL database connection parameters as a dictionary
db_config = {
    'user': 'minhly',
    'password': '22201371',
    'host': 'dbbikes.c06rsktpo8sk.us-east-1.rds.amazonaws.com',
    'database': 'dbbikes',
    'port': 3306
}

# Create a connection pool to the MySQL database
pool_name = 'dbbikes_pool'
conn_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=pool_name, pool_size=5, **db_config)


@app.route('/data')
def station_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = 'SELECT * FROM station'
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    query = request.args.get('query')
    filter_criteria = request.args.get('filter')
    if query and filter_criteria:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(prepared=True)

        query = f"SELECT * FROM station WHERE {filter_criteria} LIKE %s"
        search_query = f"%{query}%"
        cursor.execute(query, (search_query,))

        search_results = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('data.html', data=data, search_results=search_results, query=query, filter_criteria=filter_criteria)
    else:
        return render_template('data.html', data=data, query=query, filter_criteria=filter_criteria)


@app.route('/')
def index():
    # Set up the Google Maps client
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

    # Fetch the station data from the MySQL database
    conn = conn_pool.get_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM station'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Set up the markers
    markers = []
    for station in data:
        marker = {
            'position': {'lat': station[7], 'lng': station[8]},
            'title': station[6],
            'status': station[9],
            'bike_stands': station[3]
        }
        markers.append(marker)

    # Render the template with the map options, API key, and markers
    return render_template("map.html", map_options=map_options, api_key=api_key, markers=markers)


if __name__ == '__main__':
    app.run(debug=True)
