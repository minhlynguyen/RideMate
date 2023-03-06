import config
from sqlalchemy import create_engine,text
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
# from IPython.display import display

try:
    engine = create_engine(
        "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)
except Exception:
    engine = create_engine(
        "mysql://{}:{}@{}:{}/{}".format(config.USER, config.PASSWORD, config.URI, config.PORT, config.DB), echo=True)

# Test the database connection
def main() :
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SHOW VARIABLES"))
            print(list(res))
    except:
        print(traceback.format_exc())
    return 

if __name__ == '__main__':
    main()


def create_table():    
    sql = """CREATE DATABASE IF NOT EXISTS dbbikes"""
    engine.execute(sql)

    for res in engine.execute("SHOW VARIABLES"):
        print(res)

    sql = """
    CREATE TABLE IF NOT EXISTS station
    (
    address VARCHAR(256),
    banking INTEGER,
    bike_stands INTEGER,
    bonus INTEGER,
    contract_name VARCHAR(256),
    name VARCHAR(256),
    number INTEGER NOT NULL,
    position_lat REAL,
    position_lng REAL,
    status VARCHAR(256),
    last_update INTEGER UNSIGNED NOT NULL,
    db_update INTEGER UNSIGNED NOT NULL
    PRIMARY KEY (number, last_update, db_update)
    )
    """
    try:
        res = engine.execute("DROP TABLE IF EXISTS station")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    sql = """
    CREATE TABLE IF NOT EXISTS availability
    (
    number INTEGER NOT NULL,
    available_bikes INTEGER,
    available_bike_stands INTEGER,    
    last_update INTEGER UNSIGNED NOT NULL,
    status VARCHAR(256),
    db_update INTEGER UNSIGNED NOT NULL,
    PRIMARY KEY (number, last_update, db_update)
    )
    """
    try:
        res = engine.execute("DROP TABLE IF EXISTS availability")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    sql = """
    CREATE TABLE IF NOT EXISTS `dbbikes`.`weather_current` (
    `station` INT NOT NULL,
    `last_update` INT UNSIGNED NOT NULL,
    `temperature` DOUBLE NULL,
    `weathercode` INT NULL,
    `windspeed` DOUBLE NULL,
    db_update INTEGER UNSIGNED NOT NULL
    PRIMARY KEY (`station`, `last_update`, db_update));
    """

    # sql 
    try:
        res = engine.execute("DROP TABLE IF EXISTS weather_current")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    sql = """
     CREATE TABLE `dbbikes`.`weather_forecast_24h` (
     `station` INT NOT NULL,
     `last_update` INT UNSIGNED NOT NULL,
     `forecast_time` INT UNSIGNED NOT NULL,
     `temperature` DOUBLE NULL,
     `precipitation` INT NULL,
     `weathercode` INT NULL,
     `windspeed` DOUBLE NULL,
     PRIMARY KEY (`station`, `last_update`, `forecast_time`));
     """

    # sql 
    try:
        res = engine.execute("DROP TABLE IF EXISTS weather_forecast_24h")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

    sql = """
     CREATE TABLE `dbbikes`.`weather_forecast_7d` (
     `station` INT NOT NULL,
     `last_update` INT NOT NULL,
     `forecast_day` INT NOT NULL,
     `weathercode` INT NULL,
     `temperature_max` DOUBLE NULL,
     `temperature_min` DOUBLE NULL,
     PRIMARY KEY (`station`, `last_update`, `forecast_day`));"""

    try:
        res = engine.execute("DROP TABLE IF EXISTS weather_forecast_7d")
        res = engine.execute(sql)
        print(res.fetchall())
    except Exception as e:
        print(e)

# If need to redesign/delete the table, run this function.
# create_table()
