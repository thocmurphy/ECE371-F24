### SyncTimeWithAT.py
 - Connects board to network and uses an AT command to ask the network for the time and then sets the board's time with it
 - Works correctly, but does not give millisecond precision (impractical for drift calculations)

### UDPSocketWithAT.py
 - Attempts to define a PDP context that is compatible with UDP connections
 - Attempts to establish a UDP socket with pool.ntp.org NTP server but fails
