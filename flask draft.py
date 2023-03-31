
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
