# Authentication module
# OpenRS v 0.1.0
# Author: William Barr

import config
import dbservices
import hashlib
import logging

SALT_TEXT = config.options["Salt"]

def doSalt(presalt):
    presalt +=SALT_TEXT
    presalt = bytes(presalt, 'utf-8')
    salted_hash = hashlib.sha256(presalt)
    salted_hash = salted_hash.hexdigest()
    return salted_hash

def addUser(username, pwhash, groupid):
    salted_hash = doSalt(pwhash)
    cur = dbservices.getCursor()


    sql = "INSERT INTO `users` (`username`, `password`, `group_id`) VALUES(%s, %s, %s)"
    cur.execute(sql, (username, salted_hash, groupid))
    dbservices.closeCursor(cur)
    logging.info("User %s added to group %i", username, groupid)
    
def checkIfUsernameExists(username):
    cur = dbservices.getCursor()

    sql = "SELECT COUNT(*) FROM `users` WHERE `username` = %s"
    cur.execute(sql, username)
    numEntries = cur.fetchone()[0]
    
    dbservices.closeCursor(cur)

    if numEntries:
        return True
    return False
    
def loginUser(username, pwhash):
    salted_hash = doSalt(pwhash)
    
    sql = "SELECT COUNT(*) FROM `users` WHERE username = %s AND password = %s"
    
    cur = dbservices.getCursor()
    cur.execute(sql, (username, salted_hash))
    numrows = cur.fetchone()[0]
    dbservices.closeCursor(cur)
    if numrows:
        logging.info("User %s successfully logged in", username)
        return True
    logging.info("User %s login attempt failed", username)
    return False

def deleteUser(username):
    sql = "DELETE FROM `users` WHERE username = %s"
    cur = dbservices.getCursor()
    rows_affected = cur.execute(sql, username)
    dbservices.closeCursor(cur)
    if rows_affected:
        logging.info("User %s deleted.", username)
        return True
    logging.info("User %s deletion failed.", username)
    return False

def editUser(orig_username, username, pwhash, groupid):
    sql = "UPDATE `users` SET `username` = %s, `password` = %s, `group_id` = %s WHERE `username` = %s"
    cur = dbservices.getCursor()
    rows_affected = cur.execute(sql, (username, doSalt(pwhash), groupid, orig_username))
    dbservices.closeCursor(cur)
    if rows_affected:
        logging.info("User %s edited: Group %s", username, groupid)
        return True
    logging.info("User %s editing failed", username)
    return False
