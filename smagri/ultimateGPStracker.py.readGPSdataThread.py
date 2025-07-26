# NOTE: heading is  azimuth, which is from north and clockwise to the angle

# GPGGA,010039.000,3346.5863,S,15058.1509,E,2,09,1.05,92.3,M,21.9,M,,*48

#       UTCtime,latitude, N/S hemisphere, longitude, E/W hemisphere,
#       do we have a fix(indicates accuracy, 1=normal GPS 5-10m,
#       2=differential fix 1-3m), number of satellites used for fix,
#       how diluted and the lower the number the better,our actual
#       elevation in meters given the number of sattilites we have(you
#       need >5 for a good fix).

# The adafruit ultimate GPS version supports the GPS(USA), the
# original GPS system which is one of 5 GPS systems in use today.

# Satellite System	Supported?
#GPS (USA)	✅ Yes
#GLONASS (Russia)	❌ No
#Galileo (EU)	❌ No
#BeiDou (China)	❌ No
#QZSS (Japan)	❌ No

#
# $GPGSV,4,1,16,30,71,159,22,14,65,249,16,22,48,277,19,07,48,090,22*79
#
# num messages, message number, num  satellites in view, satellite num
# fixed to, elevation,  azimuth is a bearing or  measurment from north
# to east, signal strength  in dB, 20-30 is a weak  signal - btw 30-40
# good  signal -btw  40-50  is a  very good  signal  then repeat  from
# sattilite number, elevation, azimuth

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



from machine import Pin, I2C, UART
import time
import _thread

# create GPS object
GPS = UART(1, baudrate = 9600, tx=machine.Pin(8), rx=machine.Pin(9))

# create the atomic lock in python, in c++ we put dataLock definition
# in header file.
dateLock = _thread.allocate_lock()

# we can shutdown the thread with Ctrl-C cleanly, like the destructor
# in c++
keepRunning = True

# this is a python dictionary, like an array combined with a map in c
# and c++ index=GPGGA, data=="" at this stage
#
# The raw NMEAdata
NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
    }

# interpreted GPS UART data output lines/NMEAdata data lines
GPSdata = {
    'latDD' : 0,
    'lonDD' : 0,
    'heading' : 0,
    'fix' : False,
    'sats' : 0,
    'knots' : 0
    }


# This is the  reading NMEAdata thread.  NMEAdata comming  for the GPS
# module via  a uart.  We  put this  in a thread  as we don't  want to
# loose data while processing it.

def readGPSdataThread():
    print("Thread Running")
    global keepRunning, NMEAdata # NMEAdata is a dictionary, like a map in c++

    # inlitiase string KEY in the dictionary to null string.
    # dictionary definition, Key=NMEAdata read from GPS uart.
    GPGGA = ""
    GPGSA = ""
    GPRMC = ""
    GPVTG = ""
    # do nothing if there is no data in the buffer
    while not GPS.any():
        pass
    # now we have data, read buffer till it's empty, the stale
    # data, this clears the buffer
    while GPS.any():
        junk=GPS.read()
        print(junk)
        myNMEA = "" # initialise the NMEA string read from uart

        while keepRunning:
            # we only read NMEA data when it's present in the buffer
            if GPS.any():
                # Read one byte at a time, ie one char at a time till
                # EOL, and decode it from a byte to a string using
                # utf-8 codec(ASCII is a subset of UTF-8)
                myChar=GPS.read(1).decode('utf-8')
                # supress line feed, so you can contiue to read accross
                # print(myChar, end="")
                myNMEA+=myChar
                if myChar == '\n':
                    # When EOL is reached strip the EOL char from myNMEA string.
                    myNMEA = myNMEA.strip() 
                    # store the NMEAdata strings into variables
                    if myNMEA[1:6] == "GPGGA":
                        GPGGA = myNMEA
                    if myNMEA[1:6] == "GPGSA":
                        GPGSA = myNMEA
                    if myNMEA[1:6] == "GPRMC":
                        GPRMC = myNMEA
                    if myNMEA[1:6] == "GPVTG":
                        GPVTG = myNMEA

                    # if _all_  the NMEA data is  present populate the
                    # dictionary  NMEAdata. ie  setup the  map between
                    # key=type of NMEA string = string of data
                    if GPGGA != "" and GPGSA!="" and GPRMC!="" and GPVTG!="":
                        # we must do this within a lock as other
                        # threads may want to access the NMEAdata
                        # dictionary elements at the same time
                        dataLock.acquire()
                        NMEAdata = {
                            'GPGGA' : GPGGA,
                            'GPGSA' : GPGSA,
                            'GPRMC' : GPRMC,
                            'GPVTG' : GPVTG
                        }
                        dataLock.release()
                    
            myNMEA = "" # reset to read the next NMEA data string
    print("Thread Terminated Cleanly")
# end: gpsThread ###############################################################

# # do nothing if there is no data in the buffer
# while not GPS.any():
#     pass
# # now we have data, read buffer till it's empty, the stale data
# while GPS.any():
#     junk=GPS.read()
#     print(junk)


# # now we have new data
# try:
#     while True:
#         # If any GPS signal exists, read a char/1 byte and print it
#         if GPS.any():
#             myChar=GPS.read(1).decode('utf-8')
#             # supress line feed, so you can contiue to read accross
#             # print(myChar, end="")
#             myNMEA=myNMEA+myChar
#             if myChar == '\n':
#                 # process the entire NMEA sentence of characters
#                 # ie 1 to 5, don't include 6
#                 if myNMEA[1:6]=="GPGGA":
#                     GPGGA=myNMEA
#                     GPGGAarray=GPGGA.split(',')
#                     # print(GPGGA)
#                     # print(GPGGAarray)
#                     # we have a sattilite fix ie this value is,1,2 or 3
#                     if int(GPGGAarray[6]) != 0:
#                         latRAW=GPGGAarray[2]
#                         lonRAW=GPGGAarray[4]
#                         # it's expected that the number of satellites
#                         # will vary over time as they orbit twice per
#                         # day
#                         numSat=int(GPGGAarray[7])

#                         # these are always +ve values for N and E but
#                         # -ve for S and W
#                         #
#                         # converting RAW data to Decimal Degrees(ie
#                         # DD) for latitude and longatude
#                         #
#                         # latRAW[0:2] means 1st and the 2nd num only,
#                         # ie 0 and 1(not 2)
#                         latDD=int(latRAW[0:2])+float(latRAW[2:])/60
#                         lonDD=int(lonRAW[0:3])+float(lonRAW[3:])/60
#                         # prime meridian runs through grenich in england
#                         if GPGGAarray[3]=='S': # south of the equator
#                             latDD=-latDD
#                         if GPGGAarray[5]=='W': # west of the prime meridian
#                             lonDD=-lonDD
#                         print("Latitude, Longitude, numberOfSattilites",
#                               latDD, lonDD, numSat)
                            
#                 if myNMEA[1:6]=="GPGSA":
#                     GPGSA=myNMEA
#                     GPGSAarray=GPGSA.split(',')
#                      # print(GPGSA)
#                     #print(GPGSAarray)
#                 if myNMEA[1:6]=="GPRMC":
#                     GPRMC=myNMEA
#                     GPRMCarray=GPRMC.split(',')
#                     #print(GPRMC)
#                     #print(GPRMCarray)
#                     knots=float(GPRMCarray[7]) # how fast we are moving
#                     heading=float(GPRMCarray[8]) # angle from north clockwise we are moving to
#                     print(knots, "Knots at a Heading of: ",heading)
#                 if myNMEA[1:6]=="GPVTG":
#                     GPVTG=myNMEA
#                     GPVTGarray=GPVTG.split(',')
#                     #print(GPVTG)
#                     #print(GPVTGarray)
#                 if myNMEA[1:6]=="GPGSV":
#                     GPGSV=myNMEA
#                     GPGSVarray=GPGSV.split(',')
#                     #print(GPGSV)
#                     #print(GPGSVarray)
#                     if GPGGA!="":
#                         # if the number of sattellites for no fix=0
#                         if int(GPGGAarray[6])==0:
#                             # as more sattellites come in to view they
#                             # are logged here. So we can see it's
#                             # progressing towards a fix.
#                             print('Aquiring Fix:', GPGSVarray[3], "Sattellites in View")
                    
#                 # reset for next NEMA sentence
#                 myNMEA=""



###############################################################################
#                                   main.cpp                                  #
###############################################################################

# launch the reading data thread
_thread.start_new_thread(readGPSdataThread, ())
time.sleep(2)
try:
    while True:
        # dataLock.acquire()
        # NMEAmain = NMEAdata.copy()
        # dataLock.release()
        # #parseGPS()
        # if GPSdata['fix'] == False:
        #     print("Waiting for Fix . . .")
        # if GPSdata['fix'] == True:
        #     print(" Ultimate GPS Tracker Report: ")
        #     print("Lat and Lon: ",GPSdata['latDD'],GPSdata['lonDD'])
        #     print("Knots: ",GPSdata['knots'])
        #     print("Heading: ",GPSdata['heading'])
        #     print("Sats: ",GPSdata['sats'])
        #     print()
 
        time.sleep(10)
        
# This MicroPython code block is part of an except clause that handles
# a KeyboardInterrupt — typically triggered when you press Ctrl+C on
# your keyboard to stop a running script.

except KeyboardInterrupt: # catches the Keyboardinterrupt exception to
                          # the program can exit gracefully instead of
                          # crashing If we get a lockup it allows you
                          # to use the keyboard to interrupt it
                          # keyboardinterrupt may be just a ctrl-C

    keepRunning = False # kill main thread 

    print("\nStopping Program . . . Cleaning Up UART")
    # we don't know why sleeps don't work here but do in paul's code
#    time.sleep(1) # short pause to ensure clean shutdown

    # This deinitializes the UART interface, freeing hardware
    # resources and avoiding interference with other parts of the
    # system.
    GPS.deinit() # properly release UART before exit

#    time.sleep(1) # short pause to ensure clean shutdown        

    print("Exited Cleanly")
     
    
