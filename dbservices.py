# Database Services module
# OpenRS v 0.1.0
# Author: William Barr

import config
import pymysql
import logging
import threading



dbconnection = None
opencursors = []

accesslock = threading.Lock()

def getCursor():
    global dbconnection
    global opencursors
    
    accesslock.acquire()
    if dbconnection == None:
        dbconnection = pymysql.connect(host = config.options["DBHost"], user = config.options["DBUser"], passwd = config.options["DBPass"], db = config.options["DBName"])
    cursor = dbconnection.cursor()
    opencursors.append(cursor)
    accesslock.release()
    return cursor

def closeCursor(cursor):
    global dbconnection
    global opencursors

    
    accesslock.acquire()
    dbconnection.commit()
    cursor.close()
    try:
        opencursors.remove(cursor)
    except:
        logging.warn("Unable to remove cursor from opencursors list.")
    if(len(opencursors) == 0):
        dbconnection.close()
        dbconnection = None
    accesslock.release()

def commit():
    accesslock.acquire()
    dbconnection.commit()
    accesslock.release()
