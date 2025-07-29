from machine import Pin, UART
import time

# Adjust pins as needed for your board
GPS = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

myNMEA = ""

# Clear old data
while not GPS.any():
    pass

while GPS.any():
    junk = GPS.read()
    print(junk)

# Read new incoming sentences
try:
    while True:
        if GPS.any():
            myChar = GPS.read(1).decode('utf-8', 'ignore')
            myNMEA += myChar

            if myChar == '\n':
                print("RAW:", myNMEA)
                if len(myNMEA) >= 6:
                    sentence_type = myNMEA[1:6]
                    print("Sentence Type:", sentence_type)
                else:
                    print("Incomplete NMEA sentence:", myNMEA)

                myNMEA = ""  # Reset after sentence is complete
except KeyboardInterrupt:
    print("\n...Cleaning Up UART")
    GPS.deinit()
    time.sleep(1)
    print("Cleanly Exited UART")
