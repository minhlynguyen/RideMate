import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/station')
def station_page():
    db = mysql.connector.connect(host="dbbikes.cbqpbir87k5q.eu-west-1.rds.amazonaws.com",
                                 user="fei", passwd="22200125", db="dbbikes", port=3306)
    cur = db.cursor()

    sql = ("""SELECT * FROM station""")

    cur.execute(sql)
    results = cur.fetchall()
    db.close()
    return render_template('station.html', station=results)


# Replace YOUR_API_KEY with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyC52j5KuFhqFUz3qfPc7s16bmfqRLb9wy8"

@app.route('/')
def index():
    return render_template('home.html', api_key=GOOGLE_MAPS_API_KEY)

if __name__ == '__main__':
    app.run(debug=True)