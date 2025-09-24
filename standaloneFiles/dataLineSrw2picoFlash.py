# This code writes  three sets of sensor readings to  a logfile on the
# Pico W,  each set  as a  comma-separated line,  overwriting previous
# content, then reads the file back  line by line, splitting each line
# into  a list.   Purpose: Show  how to  log multiple  data sets  to a
# logfile and read them one line at a time.

# Writing one sensorData line at a time:

readingsOne = ["25.5", "26.0", "24.8"]  # List of First set of sensor readings
readingsTwo = ["12.6", "62.5", "33.4"]  # List of Second set of sensor readings
readingsThree = ["19.8", "20.1", "21.3"]# List of Third set of sensor readings

# Combine all the readings into a list of lists/like an array of
# arrays(a multidimensional array).
allReadings = [readingsOne, readingsTwo, readingsThree]

 # Open logfile in write mode ('w'), this overwrites all data
 # previously in the file.
with open('dataLineSrwLog.txt', 'w') as fileRWpicoFlash:

    # Loop through each set of readings
    for readingSet in allReadings:
        # Convert reading sets to a comma seperated list for easier
        # parsing.
        
        # ','.join(readingSet)  converts  the   list  (e.g.,  ["25.5",
        # "26.0", "24.8"]) into a  single string "25.5,26.0,24.8" with
        # commas    between   values.     We    need   this    because
        # fileRWpicoFlash.write() REQUIRES A STRING, not a list.
        readingsSetCSVstrLine = ','.join(readingSet)
        print("Sensor values as List: ", readingSet)
        print("Sensor values as csv string: ", readingsSetCSVstrLine)
        # Write the line to the file with a newline
        fileRWpicoFlash.write(readingsSetCSVstrLine + '\n')
# Confirm data was written
print("Written all 3 sensor readings in list format to dataLineSrwLog.txt\n"
      "as csv string.")




# Reading one line at a time
print("\nRead dataLineSrwLog.txt sensor data lines in csv format strings and\n"
      "converted them to sets of lists:")

 # Open logfile in read mode ('r')
with open('dataLineSrwLog.txt', 'r') as fileRWpicoFlash:

    #print("Reading line by line:")
    # Loop through each line in the file
    for readingsSetCSVstrLine in fileRWpicoFlash:

        # Lets  do something  to  our  raw data  line  in logfile  for
        # demonstartion, or as an exercise.
        
        # line.strip() removes leading/trailing whitespace, including '\n'
        # .split(',') splits the line at commas to create a list of values
        readingsSet2listLine = readingsSetCSVstrLine.strip().split(',')
        # Print the list of readings
        print("Sensor readings:", readingsSet2listLine)


print("\nNOTE:")
print("In micropython the file .write() and .read() meathods operate only on\n"
      "strings.\n")
print("Except when a file is open in binary mode, where you read and write\n"
      "bytes.")
