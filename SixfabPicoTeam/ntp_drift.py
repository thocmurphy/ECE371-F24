"""
Utilizes ntp_utils module to connect to network, set board time, measure drift over WAIT_PERIOD intervals.
Outputs board ms time, ntp server ms time, and difference/drift to time_drift.csv.
Use keyboard interrupt to stop script
"""
import ntp_utils
import json
import machine
import time

MINUTES = 5
WAIT_PERIOD = MINUTES * 60

rtc = machine.RTC()

# Get WiFi Credentials with YAML
with open("credentials.json", "r") as file:
    credentials = json.load(file)

ssid = credentials["Wifi_Name"]
password = credentials["Wifi_Password"]
host = credentials["NTP_Host"]

# Connect board to WiFi
ntp_utils.connect_network(ssid, password)

# Create text file with headers
with open('time_drift.csv', 'w') as file:
    file.write("Board_Time, NTP_Time, Difference\n")

# Set the time of the board
print("Attempting to set board's time.", end="")
for i in range(10):
    try:
        ntp_utils.set_time(host)
        break
    except:
        time.sleep(1)
        print(".", end="")

# Verify the time was set
current_time = rtc.datetime()
print(f"\nBoard time set to: {current_time}\n")

# Start monitoring loop
try:
    while True:
        # Try to get time from the server, if there is an error then restart the loop
        try:
            ntp_s, ntp_ms = ntp_utils.get_time(host) # Get time from NTP server
            board_time = time.time_ns() // 10**6 # Get time from board

            ntp_ms = ntp_ms + (ntp_s * 1000) # Convert time to milliseconds

            diff_ms = abs(board_time - ntp_ms) # Find time difference in milliseconds
            
            output_line = "%s, %s, %s\n"%(board_time, ntp_ms, diff_ms) # Format output line
            
            # Write to text file
            with open('time_drift.csv', 'a') as file:
                file.write(output_line)
            
            print(output_line)
        except:
            print("Error in monitoring loop.\n")
            
        # Wait for specified period
        time.sleep(WAIT_PERIOD)
        
except (KeyboardInterrupt, SystemExit, Exception):
    print("\nMonitoring stopped")
