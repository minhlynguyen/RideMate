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


app.run()
