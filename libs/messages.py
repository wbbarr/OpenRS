# Messages module
# OpenRS v 0.1.0
# Author: William Barr

## Header message is in network format;
## Message ID (Unsigned short) followed by unsigned int message len. 

HEADER_STRUCT = "!HI"

#MESSAGE IDs:
#ID 0: Heartbeat message; no payload.
#ID 1: Login (Username)
#ID 2: Login (Password & Token)
#ID 3: Close Session

MESSAGES = ("", "!30s", "!64sI", "")
