# SSL Server module
# OpenRS v 0.1.0
# Author: William Barr

import config
import logging
import ssl
import socket
import threading
import sys
from multiprocessing import Queue

            
class ServerListener(threading.Thread):
    def run(self):
        commandQueue = Queue()
        print(config.options)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.load_cert_chain(certfile = config.options["CertFile"], keyfile = config.options["KeyFile"])
        
        bindsocket = socket.socket()
        bindsocket.bind((config.options["Domain"], int(config.options["ListenPort"])))
        bindsocket.listen(5)
        
        logging.info("Now accepting connections")
        acceptConnections = True

        while acceptConnections:
            newsocket, fromaddr = bindsocket.accept()
            logging.debug("Accepted connection from %s", str(fromaddr))
            connstream = context.wrap_socket(newsocket, server_side = True)
            logging.debug("Completed handshake with %s", str(fromaddr))
            try:
                connstream.shutdown(socket.SHUT_RDWR)
                connstream.close()
                logging.info("Successfully completed connection shutdown with %s", str(fromaddr))
            except:
                logging.error("Had a problem with a client!")
                
        logging.info("Connection listener process terminating.")        




def handleClientProcess(socketnamespace, commandQueue):
    pass
