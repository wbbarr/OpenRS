# Server Main module
# OpenRS v 0.1.0
# Author: William Barr

#This is the entry point for the server.

import config
import logging
import sys
import threading
from multiprocessing import Manager, Process, Pipe


class ServerShellDisplayThread(threading.Thread):
    def __init__(self, parentShellPipe):
        super().__init__()
        self.parentShellPipe = parentShellPipe
        
    def run(self):
        stillRunning = True
        while stillRunning:
            data = str(self.parentShellPipe.recv())
            if(data == "quit"):
                stillRunning = False
            logging.info("Shell: %s", data)
            print(">>  {0}".format(data))

class ServerShellInputThread(threading.Thread):
    def __init__(self, childShellPipe, childShellPipeLock, serverShellParentPipe):
        super().__init__()
        self.childShellPipe = childShellPipe
        self.childShellPipeLock = childShellPipeLock
        self.serverShellParentPipe = serverShellParentPipe
    def run(self):
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


if __name__ == "__main__":
    masterMgr = Manager()

    #Read the configuration file
    config.readConfigFile()
    parentShellPipe, childShellPipe = Pipe()
    childShellPipeLock = masterMgr.Lock()
    serverShellParentPipe, serverShellChildPipe = Pipe()

    displayThread = ServerShellDisplayThread(parentShellPipe)
    displayThread.start()
    inputThread = ServerShellInputThread(childShellPipe, childShellPipeLock, serverShellParentPipe)
    
    inputThread.start()


    
    
else:
    logging.error("Shouldn't import servermain as a module.")
