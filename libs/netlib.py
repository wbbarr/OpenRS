# Networking Library
# OpenRS v 0.1.0
# Author: William Barr


"""
Gets a message of length bytesToRecv.  Returns bytes of message or None
if message times out.
TODO: Handle Socket errors.
"""
def receiveMessage(self, bytesToRecv):
    bytesrecvd = b''
    
    #Will continue looping until all bytes are received or select times out.  
    while len(bytesrecvd) < bytesToRecv):
        res = select([self.clientSock], [], [], 30.0)
        if(len(res[0]) == 0):
            return None
        bytesrecvd += self.clientSock.recv(bytesToRecv-len(bytesrecvd))
        
    return bytesrecvd
