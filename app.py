from sqlalchemy import create_engine,text
from flask import Flask, render_template, jsonify
import traceback
import sys
import config
import time
import requests
import json
import functools

app = Flask(__name__)

def get_db():
    try:
        engine = create_engine(
            "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)
        return engine
    except:
        engine = create_engine(
            "mysql://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)
        return engine
    
@app.route("/stations")
@functools.lru_cache(maxsize=128)
def get_stations():
    engine = get_db()
    sql = "select * from station;"
    try:
        with engine.connect() as conn:
            rows = engine.execute(text(sql)).fetchall()
            print('#found {} stations', len(rows), rows)
            return jsonify([row._asdict() for row in rows]) # use this formula to turn the rows into a list of dicts
    except:
        print(traceback.format_exc())
        return "error in get_stations", 404

# get_stations()