# SSL Server module
# OpenRS v 0.1.0
# Author: William Barr

import config
import logging
import ssl
import socket
from multiprocessing import Manager



def startServer():


    #Starting server
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.load_cert_chain(certfile = config.options["CertFile"], keyfile = config.options["KeyFile"])

    bindsocket = socket.socket()
    bindsocket.bind((config.options["Domain"], int(config.options["ListenPort"])))
    bindsocket.listen(5)

    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side = True)
        
