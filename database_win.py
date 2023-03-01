import sqlalchemy
from sqlalchemy import create_engine, text
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
# 
# from IPython.display import display
# import mysql.connector
# import ssl


URI = "dbbikes.c06rsktpo8sk.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
USER = "minhly"
PASSWORD = "22201371"
engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

def main() :
#     try:
#     res = engine.execute("DROP TABLE IF EXISTS station")
#     res = engine.execute(sql)
#     print(res.fetchall())
# except Exception as e:
#     print(e)
    #sql = """CREATE DATABASE IF NOT EXISTS dbbikes"""
    #engine.execute(sql)
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SHOW VARIABLES"))
            print(list(res))
    except:
        print(traceback.format_exc())
    return 
sql = """
CREATE TABLE IF NOT EXISTS station
(
address VARCHAR(256),
banking INTEGER,
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(256),
name VARCHAR(256),
number INTEGER,
position_lat REAL,
position_lng REAL,
status VARCHAR(256)
)
"""
if __name__ == '__main__':
    main()
