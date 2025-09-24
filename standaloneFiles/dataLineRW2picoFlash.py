# This code writes  three sensor readings as  a comma-separated string
# to a logfile on the Pico W,  then reads the file back and splits the
# string into  a list.   Purpose: Demonstrate  basic file  writing and
# reading in MicroPython using a logfile.

# Writing comma-delimited data to a file. Example sensor temperature
# readings from three sensors
sensorData = "25.5,26.0,24.8" 

# Get object/handle to the logfile, can be named anything,
# fileRWpicoFlash, Open logfile in write mode ('w').
with open('dataLineRWlog.txt', 'w') as fileRWpicoFlash:
    # Write the comma-separated string to the file
    fileRWpicoFlash.write(sensorData)
# Confirm data was written    
print("csv Sensor Data string written to dataLineRWlog.txt")



# Reading comma-delimited data

# NOTE: mycropython can  use single quotes or double  quotes but don't
# mix  them.  with  open,  takes  care of  closing  the  file  at  the
# appropriate time so you don't have to close them.

# Open logfile in read mode ('r')
with open('dataLineRWlog.txt', 'r') as fileRWpicoFlash:
    rawData = fileRWpicoFlash.read()  # Read the entire file as a string
    print("Raw data read from dataLineRWlog.txt:", rawData)

    # Lets do something with our raw data for demonstration.  Hence, parse
    # into a list/array.

    # Split the string at commas to create a list/array of strings.
    rawData2rayStrs = rawData.split(',')
    # Print the resulting list
    print("Parsed raw data into list/array of strings:", rawData2rayStrs)
