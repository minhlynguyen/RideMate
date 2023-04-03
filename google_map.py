from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyC52j5KuFhqFUz3qfPc7s16bmfqRLb9wy8"
GoogleMaps(app)


@app.route('/')
def mapview():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    return render_template('map.html', mymap=mymap)


if __name__ == '__main__':
    app.debug = True
    app.run()
