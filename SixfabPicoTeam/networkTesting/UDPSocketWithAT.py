"""
Uses PicoLTE module and atcom.send_at_comm() function to send AT commands.
Commands ATTEMPT to connect board to network and make a valid UDP socket with an NTP server.
"""
from pico_lte.core import PicoLTE
import time
import json
import machine

with open("credentials.json", "r") as file:
    credentials = json.load(file)

apn = credentials["APN"]

picoLTE = PicoLTE()

AT_commands = ['AT+QIACT?', 'AT+QIOPEN=1,1,"UDP SERVICE", "pool.ntp.org",123,0,1']
"""
AT+QIACT?:
Checks the parameters needed for a UDP connection. Usually opened automatically by PicoLTE module.
Usually 1,1,1,IP. Where the ones mean context ID (1-16), context state (1 for activated, 0 for not),
context type (1 for IPv4 and 2 for IPv6) respectively.

'AT+QIOPEN=1,1,"UDP SERVICE","pool.ntp.org",123,0,1':
Attempts to open a UDP socket with the pool.ntp.org NTP server. Parameters in order are:
contextID, connect ID, service type, IP address/domain_name, remote port, local port, access mode.
We have not been able to get this to work.

More info in the documentation here:
https://sixfab.com/wp-content/uploads/2023/05/Quectel_BG95BG77BG600L_Series_TCPIP_Application_Note_V1.2.pdf
"""

for comm in AT_commands:
    res = picoLTE.atcom.send_at_comm(comm)
    print(res)
    time.sleep(1)