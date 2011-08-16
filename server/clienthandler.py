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
            #First, receive a header message
            header = self.receiveMessage(struct.calcsize(messages.HEADER_STRUCT))
            header = struct.unpack(messages.HEADER_STRUCT, header)

            payload = self.receiveMessage(struct.calcsize(messages.MESSAGES[header[0]]))
            if(len(payload) > 0):
                payload = struct.unpack(messages.MESSAGES[header[0]], payload)
            else:
                payload = ()
            if(header[0] == 3):
                keepChecking = False
            self.commandQueue.put((header[0], payload))

        #Still might be something left to send; only close reading buffer.  Socket will be closed by worker thread after sends completed.  
        self.clientSock.shutdown(socket.SHUT_RD)

    # Gets a message of length bytesToRecv.  Returns bytes of message or None
    # if message times out.
    # TODO: Handle Socket errors.  
    def receiveMessage(self, bytesToRecv):
        bytesrecvd = b''
        
        #Will continue looping until all bytes are received or select times out.  
        while len(bytesrecvd) < bytesToRecv):
            res = select([self.clientSock], [], [], 30.0)
            if(len(res[0]) == 0):
                return None
            bytesrecvd += self.clientSock.recv(bytesToRecv-len(bytesrecvd))
            
        return bytesrecvd
