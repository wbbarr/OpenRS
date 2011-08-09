# Database Services module
# OpenRS v 0.1.0
# Author: William Barr

import config
import pymysql
import logging



dbconnection = None

def getCursor():
    global dbconnection
    
    if dbconnection == None:
        dbconnection = pymysql.connect(host = config.options["DBHost"], user = config.options["DBUser"], passwd = config.options["DBPass"], db = config.options["DBName"])
        logging.info("Connected to database.")
    cursor = dbconnection.cursor()
    return cursor

def closeCursor(cursor):
    global dbconnection
    
    dbconnection.commit()
    cursor.close()

def commit():
    dbconnection.commit()
