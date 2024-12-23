"""
Uses PicoLTE module and atcom.send_at_comm() function to send AT commands.
Commands will connect board to network and then ask the 4G network for the time
and then sync.
"""
from pico_lte.core import PicoLTE
import time
import json
import machine

with open("credentials.json", "r") as file:
    credentials = json.load(file)

apn = credentials["APN"]

picoLTE = PicoLTE()

AT_commands = ["AT+CFUN=1", "AT+CGATT=1", f'AT+CGDCONT=1,"IP","{apn}"', "AT+CCLK?"]

"""
AT+CFUN=1:
Enables full functionality of the modem, allows for network connection

AT+CGATT=1:
Attatched the device to the packet-switched service of the network.
Needed for data communication (data recieving and transmitting)

AT+CGDCONT=1,"IP","APN":
Configures the packet data protocol context for the modem.
1 -> identifies the session
IP -> specifies the type of connection
super -> APN, access point name for the network

AT+CCLK?:
Asks the network for the time
"""

for comm in AT_commands:
    res = picoLTE.atcom.send_at_comm(comm)
    print(res)
    time.sleep(1)

# Sync Pico LTE board time
time_str = res['response'][0].split('"')[1] # Extract time string between quotes

date_part, time_part = time_str.split(',') # Split into date and time parts

yy, mm, dd = map(int, date_part.split('/')) # Parse date (YY/MM/DD)

# Parse time (HH:MM:SS)
time_only = time_part.split('-')[0]  # Remove part after -
HH, MM, SS = map(int, time_only.split(':'))

year = 2000 + yy # Convert 2-digit year to 4-digit

# Set RTC (year, month, day, weekday, hours, minutes, seconds, subseconds)
rtc = machine.RTC()
rtc.datetime((year, mm, dd, 0, HH, MM, SS, 0))

print(time.localtime()) # Print board time