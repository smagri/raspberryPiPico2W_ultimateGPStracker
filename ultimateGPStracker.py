# NOTE: heading is  azimuth, which is from north and clockwise to the angle

# GPGGA,010039.000,3346.5863,S,15058.1509,E,2,09,1.05,92.3,M,21.9,M,,*48

#       (1)UTCtime,(2)latitude,   (3)N/S   hemisphere,   (4)longitude,
#       (5)E/W  hemisphere, (6)do  we have  a fix(indicates  accuracy,
#       0=noFix,  1=normal   GPS  5-10m,  2=differential   fix  1-3m),
#       (7)number of  satellites used for  fix, (8)how diluted  is our
#       GPS  data.  The  lower the  number the  better, (9)our  actual
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

# (1)num  messages,  (2)message  number, (3)num  satellites  in  view,
# (4)satellite num fixed to, (5)elevation,  (6)azimuth is a bearing or
# measurment from north to east, (7)signal  strength in dB, 20-30 is a
# weak signal - btw 30-40 good signal -btw 40-50 is a very good signal
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



from machine import Pin, I2C, UART
import time
import _thread

# create GPS object
GPS = UART(1, baudrate = 9600, tx=machine.Pin(8), rx=machine.Pin(9))

# By default the  adafruit ultimate GPS reciver only  outputs a subset
# of NMEA sentences. GPVTG is disabled by default to reduce bandwidth.
# The  following line  ensures that  the  GPS reports  the GPVTG  NMEA
# sentence.   You only  need to  do  this once  so you  don't have  to
# include it in  further code.  That is, it permanantly  sets your GPS
# reciver to output GPVTG NMEA strings.

# $PMTK314,<sentence mask>*<checksum><CR><LF>
#
#
# Here is an explanation of each of the fields/sentences that can be
# enabled/disabled with the PMTK314 command.

#$PMTK314,<GLL>,<RMC>,<VTG>,<GGA>,<GSA>,<GSV>,<GRS>,<GST>,<MALM>,<MEPH>,<MDGP>,<MDBG>,<ZDA>,0,0,0,0,0,0*<Checksum>

# Even with a  fix, if the GPS is not  moving, some firmware revisions
# suppress GPVTG  because heading/course is undefined  when velocity ≈
# 0.  So we may remove this later anyhow???

# Some MTK3339 firmware  builds (the chipset in  Adafruit Ultimate GPS
# v3) are compiled with different  defaults.  If you’re using an older
# breakout  or  firmware  revision,  the  sentence  set  might  differ
# slightly, requiring explicit configuration.

GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")

# create the atomic lock in python, in c++ we put dataLock definition
# in header file.
dataLock = _thread.allocate_lock()

# we can shutdown the thread with Ctrl-C cleanly, like the destructor
# in c++
keepRunning = True

# this is a python dictionary, like an array combined with a map in c
# and c++ index=GPGGA, data=="" at this stage
#
# The raw NMEAdata
#
# This is the syntax of how you define a key,value pair in python. You
# can initialise an empty dictionary with empty_dict = {}
NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
}

# interpreted GPS UART data output lines/NMEAdata data lines into a
# dictionary of key,value pairs.  key=string, value=integer
GPSdata = {
    'latitudeDecimalDegrees' : 0,
    'longitudeDecimalDegrees' : 0,
    'heading' : 0,
    'fix' : False,
    'numSattelites4fix' : 0,
    'knots' : 0
}



# This is the  reading NMEAdata thread.  NMEAdata comming  for the GPS
# module via  a uart.  We  put this  in a thread  as we don't  want to
# loose data while processing it.

# start: readGPSdata() thread ##################################################
def readGPSdata():
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
            # EOL(in the while keepRunning loop), and decode it
            # from a byte to a string using utf-8 codec(ASCII is a
            # subset of UTF-8)
            myChar=GPS.read(1).decode('utf-8')
            # supress line feed, so you can contiue to read accross
            # print(myChar, end="")
            myNMEA+=myChar
            if myChar == '\n':
                # When EOL is reached strip the EOL char from myNMEA string.
                myNMEA = myNMEA.strip()
                # to see what NMEA data I am getting as initially we
                # weren't getting GPVTG data
                #print(myNMEA)
                # store the NMEAdata strings into variables

                # gets characters 1 to 5 in the current NMEA string
                # (it skips index 0 and stops reading at character number 5)
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
                #
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
# end: readGPSdata() thread ####################################################

# start: parseAndProcessGPSdata() function #####################################
def parseAndProcessGPSdata():
    
    # Note that in the main.py  dictionary thread NMEdata is copied to
    # NMEAmain  dictionary.  Process  the RAW  NMEA data  strings into
    # human  readable values  and  store in  GPSdata dictionary.   The
    # latitude and  longatude values are converted  to decimal degrees
    # as this  is the  standard format used  by mapping  services like
    # Google Maps, OpenStreetMap, etc.

    
    # Do we have a fix on the GPS module, 6th element in the NMEA
    # GPGGA string
    if len(NMEAmain['GPGGA'].split(',')) < 6:
        return
    readFix=int(NMEAmain['GPGGA'].split(',')[6])
    if readFix !=0:
        GPSdata['fix'] = True

        # Processing GPGGA NMEA string
        #

        # .split() splits splits the NMEA string into a list of
        # fields, using the comma as a delimiter.  The grabs the third
        # element from the NMEA string.
        #
        # Our raw latitude value, 2nd element in the NMEA string
        latitudeRAW = NMEAmain['GPGGA'].split(',')[2]

        # Takes the first two characters [0:2]
        # Takes the rest of the string [2:]
        # int() converts the first two characters to an integer
        #
        # latitude value in decimal degrees
        latitudeDecimalDegrees=int(latitudeRAW[0:2])+ float(latitudeRAW[2:])/60
        # What N/S hemisphere are we in and what is latitude in
        # Decimal Degrees.
        if NMEAmain['GPGGA'].split(',')[3] == 'S':
            latitudeDecimalDegrees = -latitudeDecimalDegrees
        GPSdata['latitudeDecimalDegrees']= latitudeDecimalDegrees

        # Our raw longatude value
        longitudeRAW=NMEAmain['GPGGA'].split(',')[4]
        #longitude value in decimal degrees
        longitudeDecimalDegrees=int(longitudeRAW[0:3]) + float(longitudeRAW[3:])/60
        # What E/W hemisphere are we in and what is longitude in
        # Decimal Degrees.
        if NMEAmain['GPGGA'].split(',')[5] == 'W':
            longitudeDecimalDegrees = -longitudeDecimalDegrees
        GPSdata['longitudeDecimalDegrees'] = longitudeDecimalDegrees

        # Number of sattilites used for fix 
        numSattelites4fix = NMEAmain['GPGGA'].split(',')[7]
        GPSdata['numSattelites4fix'] = numSattelites4fix

        # Processing GPRMC NMEA string
        #
        # Direction the GPS reciver is moving over the ground(degrees)
        # aka "course over groud (COG)". Measured in degrees from true
        # north=0deg, east=90deg, south=180deg, west=270deg
        heading = float(NMEAmain['GPRMC'].split(',')[8])
        GPSdata['heading'] = heading

        # Knot is a unit of speed of the GPS reciver is moving over
        # the ground, 1 knot=1 nautical mile per hour aka speed over
        # ground(knots). 1 knot = 1.852 km/h
        knots = float(NMEAmain['GPRMC'].split(',')[7])
        GPSdata['knots'] = knots

# end: parseAndProcessGPSdata() function #######################################



###############################################################################
#                                   main.cpp                                  #
###############################################################################

# launch the reading data thread readGPSdata()
_thread.start_new_thread(readGPSdata,())
time.sleep(2) # so we don't start reading data till there is some in
              # the UART buffer
try:
    while True:
        # You need to acquire the lock as readGPSdata() thread may be
        # using NMEAdata dictionary.  That is populating NMEAdata with
        # GPS reciver UART string values.
        dataLock.acquire()
        NMEAmain = NMEAdata.copy()
        dataLock.release()
        #print(NMEAmain['GPGGA'])
        parseAndProcessGPSdata()
        if GPSdata['fix'] == False:
            print("Waiting for Fix . . .")
        else:
            # we have a fix

            # NOTE, the  more sattilites we  get for our fix  the more
            # accurate the  position, ie latitude and  longitude.  You
            # can verify this on google earth or openstreetmap.
            
            print("We have a satellite fix, Ultimate GPS Tracker Report: ")
            # we extract latitude and longitude in the format of
            # openstreetmap and google earth
            print("Latitude and Longitude: ",
            GPSdata['latitudeDecimalDegrees'],
            GPSdata['longitudeDecimalDegrees'])
            
            print("Knots: ", GPSdata['knots'])
            print("Heading: ", GPSdata['heading'])
            print("NumSattelites4fix: ", GPSdata['numSattelites4fix'])
            print()

        # NOTE: this does not overflow the buffer as readGPSdata()
        # executes in another thread.
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
     
    
