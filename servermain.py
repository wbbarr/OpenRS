# Server Main module
# OpenRS v 0.1.0
# Author: William Barr

#This is the entry point for the server.

import config
import logging
import sys
import threading
import sslserver
import multiprocessing
from multiprocessing import Manager, Process, Pipe


class ServerShellDisplayThread(threading.Thread):
    def __init__(self, parentShellPipe):
        super().__init__()
        self.parentShellPipe = parentShellPipe
        
    def run(self):
        logger = multiprocessing.log_to_stderr()
        stillRunning = True
        while stillRunning:
            data = str(self.parentShellPipe.recv())
            if(data == "quit"):
                stillRunning = False
            logging.info("Shell: %s", data)
            print(">>  {0}".format(data))
        logger.info("Server Shell Display Thread terminating.")

class ServerShellInputThread(threading.Thread):
    def __init__(self, childShellPipe, childShellPipeLock, serverShellParentPipe):
        super().__init__()
        self.childShellPipe = childShellPipe
        self.childShellPipeLock = childShellPipeLock
        self.serverShellParentPipe = serverShellParentPipe
    def run(self):
        logger = multiprocessing.log_to_stderr()
        stillRunning = True

        with self.childShellPipeLock:
            self.childShellPipe.send("Shell ready.")
            
        while stillRunning:
            cmd = input("\n")
            cmd = cmd.strip()
            if(cmd == "quit"):
                stillRunning = False
            if(cmd != ""):
                logging.info(">> %s", cmd)
                with self.childShellPipeLock:
                    self.childShellPipe.send(cmd)
                serverShellParentPipe.send(cmd)
        logger.info("Server Shell Input Thread terminating.")


if __name__ == "__main__":
##    masterMgr = Manager()
##
##    #Read the configuration file
    config.readConfigFile()
    logging.info("Config read.")
##    parentShellPipe, childShellPipe = Pipe()
##    childShellPipeLock = masterMgr.Lock()
##    serverShellParentPipe, serverShellChildPipe = Pipe()
##
##    #Start the interactive shell
##    displayThread = ServerShellDisplayThread(parentShellPipe)
##    displayThread.start()
##    logger.debug("Shell display started.")
##    inputThread = ServerShellInputThread(childShellPipe, childShellPipeLock, serverShellParentPipe)
##    inputThread.start()
##    logger.debug("Shell input started.")

    #Fire up the server

    serverThread = sslserver.ServerListener()
    serverThread.start()
    serverThread.join()
