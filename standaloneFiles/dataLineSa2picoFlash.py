# This code  appends a new  set of sensor  readings to logfile  on the
# Pico W  as a comma-separated  line, checks  if the file  exists, and
# reads  the  file  line  by  line to  verify  the  append.   Purpose:
# Demonstrate  appending to  logfile,  verifying  file existence,  and
# checking contents.

import os  # Import os module for file system operations

# Appending a new set of readings to the file dataLineSrwlogfile
newReadings = ["30.1", "29.8", "31.0"]  # New set of sensor readings
try:
    # Open logfile in append mode ('a')
    with open('dataLineSrwLog.txt', 'a') as fileApicoFlash:  

        # ','.join(newReadings)  converts  the  list  (e.g.,  ["30.1",
        # "29.8", "31.0"]) into a  single string "30.1,29.8,31.0" with
        # commas    between   values.     We    need   this    because
        # fileApicoFlash.write() requires a string, not a list.
        appendLineCSVstrLine = ','.join(newReadings)
        # Append the line with a newline
        fileApicoFlash.write(appendLineCSVstrLine + '\n')
        print("Appended Line is=", appendLineCSVstrLine)
    # Confirm data was appended
    print("Appended new readings to dataLineSrwLog.txt")  
except OSError as e:
    # Handle errors like full flash
    print("Error appending to dataLineSrwLog.txt:", e)


# Read and print dataLineSrwLog.txt to verify append csv to list, as
# an exercise.
try:
    # Open logfile in read mode ('r')
    with open('dataLineSrwLog.txt', 'r') as fileApicoFlash:
        print("Verifying dataLineSrwLog.txt contents LIST line by line:")
        # Loop through each appendLine in the dataLineSrwLog.txt
        for appendLine in fileApicoFlash:
            # appendLine.strip() removes leading/trailing whitespace,
            # including '\n' .split(',') splits the appendLine at
            # commas to create a list of values
            sensorData = appendLine.strip().split(',')
            print("Sensor readings:", sensorData)  # Print the list of readings
except OSError as e:
    # Handle errors like file not found
    print("Error reading dataLineSrwLog.txt:", e)
