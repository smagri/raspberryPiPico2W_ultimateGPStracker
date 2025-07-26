from machine import Pin, I2C, UART
import time
GPS = UART(1, baudrate = 9600, tx=machine.Pin(8), rx=machine.Pin(9))

# GPGGA,010039.000,3346.5863,S,15058.1509,E,2,09,1.05,92.3,M,21.9,M,,*48

#       UTCtime,latitude, N/S hemisphere, longitude, E/W hemisphere,
#       differential fix(indicates accuracy, 1=normal GPS 5-10m,
#       2=differential fix 1-3m), number of satellites used for fix,
#       how diluted and the lower the number the better,our actual
#       elevation in meters given the number of sattilites we have(you
#       need >5 for a good fix).

# $GPGSV,4,1,16,30,71,159,22,14,65,249,16,22,48,277,19,07,48,090,22*79
#
# num  messages,  message  number,   num  satellites,  satellite  num,
# elevation, azimuth  is a bearing  or measurment from north  to east,
# signal  strength in  dB, 20-30  is a  weak signal  - btw  30-40 good
# signal -btw 40-50 is a very good signal
# then repeat from sattilite number, elevation, azimuth

# General info: 24  satellites in 6 different orbits,  they are evenly
# spaced above the earth, at  about 12,5000miles up.  Each one circles
# the globe twice  in 24hrs. Each sattilite transmits what  time it is
# and where I  am, time is based on atomic  clocks.  Remember it takes
# time to get  the signal, dist=speedOfLight*delay. With  dist you can
# draw a circle.  From 2 satellites you get you are on two points on a
# circle.  You need  3 sattilites to find your position  on the globe,
# where  all  three circles  intersect.   Your  GPS reciver  does  the
# triangulation.  However,  you may  be elevated  over the  earth, you
# need 4 sattilites  at a minimum to get elevation  of sea level/above
# the surface of the earth.  However,  how do we get time+error on our
# GPS  reciver,  this gives  us  one  more  unknown  we need  a  fifth
# satellite to get the error.  The  GPS reciver gets all data from the
# sattilites and then we can work out exactly where we are.


# Project 4:  video.  latitude is  pi/2 to  -pi/2, longitude is  PI to
# -PI, prime meridian at 0  degrees of latitude.  Counter clockwise is
# a +ve in longitude. +ve is north and east other directions are -ve.

# latitude: N/S 1st  two digits are degrees, rest  is decimal minutes.
# We need  to convert to  decimal degrees.
# longatude E/W 1st three  digits are degrees, rest is decimal minutes.

myNMEA=""
GPGGA=""
GPGSA=""
GPRMC=""
GPVTG=""
GPGSV=""
# do nothing if there is no data in the buffer
while not GPS.any():
    pass
# now we have data, read buffer till it's empty, the stale data
while GPS.any():
    junk=GPS.read()
    print(junk)

# now we have new data
try:
    while True:
        # If any GPS signal exists, read a char/1 byte and print it
        if GPS.any():
            myChar=GPS.read(1).decode('utf-8')

            myNMEA=myNMEA+myChar
            if myChar == '\n':
                print("RAW:", myNMEA)
                if len(myNMEA) >= 6:
                    sentence_type = myNMEA[1:6]
                    print("Sentence Type:", sentence_type)
                else:
                    print("Incomplete NMEA sentence:", myNMEA)
                # reset for next NEMA sentence
                myNMEA=""
except KeyboardInterrupt:
    # If we get a lockup it allows you to use the keyboard to interrupt it
    print("\n...Cleaning Up UART")
    GPS.deinit() # properly release UART before exit
    time.sleep(1) # short pause to ensure clean shutdown
    print("Cleanly Exited UART")
