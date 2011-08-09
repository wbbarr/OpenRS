# Server Configuration module
# OpenRS v 0.1.0
# Author: William Barr

import re
import logging

options = {}
logging.basicConfig(filename="openrs.log", level = logging.DEBUG, format = '%(asctime)s || %(levelname)s || %(message)s')

#Put all required config file options in the optionKeysList -- will pull out all config options during file reading.  
optionKeys = ["DBHost", "DBUser", "DBPass", "DBName", "Salt", "CertFile", "KeyFile", "Domain", "ListenPort"]

def readConfigFile():
    global options
    global optionKeys

    try:
        f = open("server.conf")
        rawContents = f.read()
        f.close()
    except IOError:
        logging.fatal("Unable to open server.conf file.")
        quit()
    else:
        for key in optionKeys:
            value = re.findall('\s*{0}\s*=\s*"(.+)"'.format(key), rawContents)
            if(len(value) == 0):
                logging.fatal("Unable to find required option %s in config file.", key)
                quit()

            options[key] = value[0]
