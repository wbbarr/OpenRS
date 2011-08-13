# Client Connection Handler module
# OpenRS v 0.1.0
# Author: William Barr

import config
import logging
import socket
import ssl
import threading
import datetime
import struct
import messages
from select import select


class ClientConnectionHandler(threading.Thread):
    def __init__(self, clientSock, commandQueue):
        self.clientSock = clientSock
        self.commandQueue = commandQueue

    def run(self):
        keepChecking = True

        while keepChecking:
            res = select([self.clientSock], [], [], 30.0)
            if(len(res[0]) == 0):
                keepChecking = False
                #Add a message to queue to signal timeout.
            else:
                
