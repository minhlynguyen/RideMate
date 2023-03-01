#!/user/bin/env/ python
import config
import sqlalchemy
from sqlalchemy import create_engine, text
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)

# Test the database connection
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
