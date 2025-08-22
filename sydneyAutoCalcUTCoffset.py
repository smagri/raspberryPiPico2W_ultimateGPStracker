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


# OLED display is an Hosyond 0.96  Inch OLED I2C Display Module 128x64
# Pixel  Screen IIC  Serial Mini  Self-Luminous Board  Compatible With
# Arduino Raspberry  PI (Blue and Yellow).   On the back of  the board
# there is  an address selector, in  this case a resistor  for address
# 0x3C.  However, it can be configured for address 0x30 also.

# circuit diagram https://toptechboy.com/wp-content/uploads/2025/06/gps-OLED.jpg
#
# Since pico is a 3.3V device 3.3V needs to be used to power I2C
# devices.

from machine import Pin, I2C, UART
import time
import _thread
from ssd1306 import SSD1306_I2C


 # UTC offset for Sydney in Australia, outside daylight saving time
 # utcOffset=10. For daylight saving time the utcOffset=11.

# When Does DST Start and End in Sydney Australia?

# Starts: First Sunday in October—at 2:00 am AEST, clocks spring forward
# to 3:00 am AEDT.

# Ends: First Sunday in April—at 3:00  am AEDT, clocks fall back to 2:00
# am AEST, giving you an extra hour.  utcOffset = 11

# create i2c2 object:

# Configure  I2C  on   BUS=1  of  the  raspberry   pi  pico.   Default
# address=0x3C, GP2  = SDA, GP3  = SCL,  clock frequency is  400kHz, a
# common fast i2c speed, aka Fast Mode.  Standard speed is 100kHz.

# NOTE: the address of  the OLED is indicated at the  back of the PCB,
# with a resistor accross two pins to indicate the address

# NOTE: use i2cObj instead of i2c as i2c may be a reserved word
# create i2cObj object of I2C micropython class
i2cObj = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
print("Scan:", i2cObj.scan())

# create display object: 128x64=columnsXlines of the SSD1306_I2C class
display = SSD1306_I2C(128, 64, i2cObj)

# create  GPS object  of the  micropython machine.UART  class with  this
# constructor.  UART class member functions  do raw serial i/o.  You can
# get chatGPT to display all the UART class member functions.
GPS = UART(1, baudrate = 9600, tx=machine.Pin(8), rx=machine.Pin(9))

########################################################################
# for all PMTK commands see - PMTK command packet-Complete-A11.pdf

# When the  power of  device (module) is  removed, any  modified setting
# will  be lost  and reset  to factory  default setting.  If the  device
# (module) has backup  power supply through VBACKUP or  coin battery, it
# will be  able to keep the  modified setting until the  backup power is
# exhausted.                 Packet               Type:                0
# ######################################################################

# You can also restore the system default NMEA settings via:
GPS.write(b'$PMTK314,-1*04\r\n')


# By default the  adafruit ultimate GPS reciver only  outputs a subset
# of NMEA sentences. GPVTG is disabled by default to reduce bandwidth.
# The  following line  ensures that  the  GPS reports  the GPVTG  NMEA
# sentence.   You only  need to  do  this once  so you  don't have  to
# include it in  further code.  That is, it permanantly  sets your GPS
# reciver to output GPVTG NMEA strings.

# Checksum calculation is the XOR of all the values between $ and *.
# $...*<checksum>\r\n

# $PMTK314,<sentence mask>*<checksum><CR><LF>
#
#
# Here is an explanation of each of the fields/sentences that can be
# enabled/disabled with the PMTK314 command. See pg 13.

#$PMTK314,<GLL>,<RMC>,<VTG>,<GGA>,<GSA>,<GSV>,<GRS>,<GST>,<MALM>,<MEPH>,<MDGP>,<MDBG>,<ZDA>,0,0,0,0,0,0*<Checksum>

# Even with a  fix, if the GPS is not  moving, some firmware revisions
# suppress GPVTG  because heading/course is undefined  when velocity ≈
# 0.  So we may remove this later anyhow???

# Some MTK3339 firmware  builds (the chipset in  Adafruit Ultimate GPS
# v3) are compiled with different  defaults.  If you’re using an older
# breakout  or  firmware  revision,  the  sentence  set  might  differ
# slightly, requiring explicit configuration.

# sjm, wrks, produces minimum number of NMEA sentences, only the onces
# we use.
GPS.write(b"$PMTK314,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")

# wrks Pauls currently, produces more that the minimum number of NMEA
# sentences we use:
#
#GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")


# Datasheet: Turn on everything (not all of it is parsed!)
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# create the atomic lock in python, in c++ we put dataLock definition
# in header file.
dataLock = _thread.allocate_lock()

# we can shutdown the thread with Ctrl-C cleanly, like the destructor
# in c++
keepRunning = True

# this is a python dictionary, like an array combined with a map in c
# and c++ index=GPGGA, data=="" at this stage
#
# The raw NMEAdata dictionary.
#
# This is  the syntax  of how you  define a key,value  pair, or  map, in
# python, in  what is called a  dictionary. You can initialise  an empty
# dictionary with empty_dict = {}

NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
}

# Interpreted GPS UART data output strings/NMEAdata data lines into a
# dictionary of key,value pairs.  key=string, value=integer, float,
# string or boolean here.  This is a python dictionary.
GPSdata = {
    'latitudeDecimalDegrees' : 0.0,
    'longitudeDecimalDegrees' : 0.0,
    'heading' : 0.0,
    'fix' : False,
    'numSattelites4fix' : 0,
    'knots' : 0.0,
    'time' : '00:00:00',
    'date' : '00/00/0000',
    'gpsElipsoidAltitude' : 0.0,
    'geoidSeperation' : 0.0,
    'trueAltitude' : 0.0,
    'altitude' : 0.0
}


def yield_thread():
    # yeild thread in micropython.  This call doesn't pause, it just
    # hands control back to the scheduler so the other threads or global
    # setting code can run.
    time.sleep_ms(0)

# This is the  reading NMEAdata thread.  NMEAdata comming  for the GPS
# module via  a uart.  We  put this  in a thread  as we don't  want to
# loose data while processing it.

# start: readGPSdata() thread ##################################################
def readGPSdata():
    # hacky time.sleep(10) as this also yeilds the thread

    # We  need  to  do  this  as  there is  a  bug  in  the  micropython
    # implementation on the raspberry pi pico  w or pico 2 w hardware we
    # are using.  See  readme file for link to issue  on the micropython
    # github page.

    # Essentially,  this  readGPSdata()  thread may  be  getting  called
    # before the main thread or  some global initialisation.  Hence, the
    # globals required  for this thread,  like keepRunning and  GPS, may
    # not be defined  when it runs.  Hence, the program  will never read
    # data as say  keepRunning is not set yet.  This  will also cause an
    # exception intermittently.  yeald_thread()  forces the other thread
    # or global initialisation  to run first.  Note  that a time.sleep()
    # here will yield this thread also.
    yield_thread()

    print("Thread Running readGPSdata")
    

    # global means use the variable values defined outside this function
    # at the global(module) level
    global keepRunning, NMEAdata, GPS # NMEAdata is a dictionary, like a map in c++

    
    # Initialise the GPS NMEA strings
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
            #print(myChar, end="")
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

                # if _all_  the NMEA ata is  present populate the
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



# user defined functions #######################################################

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
        latitudeDecimalDegrees=int(latitudeRAW[0:2]) + float(latitudeRAW[2:])/60
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
        # north=0deg, east=90deg, south=180deg, west=270deg.  True north
        # is at the north pole, magnetic north is what your compass
        # points to .
        heading = float(NMEAmain['GPRMC'].split(',')[8])
        GPSdata['heading'] = heading

        # Knot is a unit of speed of the GPS reciver is moving over
        # the ground, 1 knot=1 nautical mile per hour aka speed over
        # ground(knots). 1 knot = 1.852 km/h
        knots = float(NMEAmain['GPRMC'].split(',')[7])
        knots *= 1.852 # convert to km/h
        knots = round(knots, 3) # round the number to 3 decimal places
        GPSdata['knots'] = knots

        # convert UTS date and time to local clock date and time, including
        # offest for daylight saving or not
        utcTime = NMEAmain['GPGGA'].split(',')[1]
        utcDate = NMEAmain['GPRMC'].split(',')[9]

        time, date = UTCtoLocalDateAndTime(utcTime, utcDate)
        
        # Store local time in GPSdata dictionary
        GPSdata['time'] = time
        # Store local date in GPSdata dictionary
        GPSdata['date'] = date


        # Elevation == Altitude.  Or the height above sea level.

        # To  determine altitue  GPS uses  a mathematical  model of  the
        # earth known as  the elipsoid.  Where the north  and south pole
        # are slightly flat and the earth bulges around the equator.

        # However,  the  true altitude  factors  in  the earths  gravity
        # field(mountains,  ocean  trenches,  density variation  in  the
        # crust...etc) this  is known as  the distance above  sea level,
        # the Geoid.  Which is the sea level if the oceans were extended
        # under the land.

        # Our  GPS   module  returns  the  elipsoid   altitude  and  the
        # difference  between the  Geoid  and this  altitude, the  Geoid
        # seperation.   The Geoid  seperation is  the height  difference
        # between the ellipsoid and the Geoid at your location.

        # Thus the true altitude = altitude above elipsoid - difference
        # above the elipsoid and actual geoid altitude above sea level.
        gpsElipsoidAltitude = float(NMEAmain['GPGGA'].split(',')[9])
        geoidSeperation = float(NMEAmain['GPGGA'].split(',')[11])
        trueAltitude = gpsElipsoidAltitude - geoidSeperation
        GPSdata['gpsElipsoidAltitude'] = gpsElipsoidAltitude
        GPSdata['geoidSeperation'] = geoidSeperation
        GPSdata['trueAltitude'] = trueAltitude


        # GPS elipsoid altitude(elevation)
        altitude = float(NMEAmain['GPGGA'].split(',')[9])
        GPSdata['altitude'] = altitude

        
        # ##############################################################
        # Trying  to  get  Magnetic  Variation  and  Magnetic  Variation
        # Direction.  However,  the datasheet for the  adafruit ultimate
        # GPS version 3 does not output this data.
        ################################################################

        # Magnetic variation is the angle difference between true north
        # and magnetic north at a specific place and time.

        # True north  → the direction  along Earth’s surface  toward the
        # geographic North Pole.

        # Magnetic north → the direction your compass points, toward the
        # Earth’s magnetic north pole (which moves over time).

        # Magnetic Variation Direction +ve/E, magnetic north is east of
        # true north. -ve/W, magnetic north is wet of true north.

        # Variation changes  with location because the  earth's magnetic
        # field isn't  uniform.  Example,  Sydney, AU  in 2025  → ~12.2°
        # East.

        # Magnetic variation (and its  east/west direction) is important
        # because it’s the correction factor that links GPS-based “true”
        # headings to compass-based “magnetic”  headings — and those are
        # used in different situations.

        # GPS & maps: Use true north.
        # Magnetic compass: Points to magnetic north.

        # If you’re navigating with both, you need to know how to
        # convert between them so your bearings match.

        # Example:

        # GPS says: “Go 100° true.”
        # Your compass reads magnetic, and your location has 10° East variation.
        # You must steer 90° magnetic for your path to match 100° true.
        
        # print("GPRMC:", NMEAmain['GPRMC'])
        # magVar = NMEAmain['GPRMC'].split(',')[10]
        # print("magVar", magVar)
        # magDir = NMEAmain['GPRMC'].split(',')[11]
        # print("magDir", magDir)
        # GPSdata['Mag VarDir'] = magVar
        

        
        
# end: parseAndProcessGPSdata() function #######################################



def displayOLED():

    # Display the following  GPS data on the ssd1306 OLED.  This OLED is
    # 128x64 with  each character  being 8x8 pixels.  (0,0) is  top left
    # hand corner of screen.

    # display.text(text, column, row) where 0,0 is the top left
    # hand corner of the display
    
    display.fill(0) # blank it out
    if GPSdata['fix'] == False:
        # we don't have a fixed
        display.text("Wait for fix...", 0, 0)
    else:
        # we have a fix

        if screenOne==True:
            #display.text("ULTIMATE GPS: ", 0, 0)
            display.fill(0) # so one screen doesn't override the other
            display.text(GPSdata['date'][0:5] + ' ' + GPSdata['time'], 0, 0)
            display.text("Num Fix Sats:" + str(GPSdata['numSattelites4fix']), 0, 8)
            display.text("Lat:" + str(GPSdata['latitudeDecimalDegrees']), 0, 16)
            display.text("Long:" + str(GPSdata['longitudeDecimalDegrees']), 0, 24)
            display.text("Speed:" + str(GPSdata['knots']) + 'km/h', 0, 32)
            display.text("Head:" + str(GPSdata['heading']) + 'deg', 0, 40)
            #display.text("Mag VarDir:" + str(GPSdata['Mag VarDir']), 0, 48)
            display.text("TrueAlt:" + str(GPSdata['trueAltitude']) + 'm', 0, 48)
            display.text("GPSAlt:" + str(GPSdata['altitude']) + 'm', 0, 56)
        else:
            # goto next page
            display.fill(0)
            display.text(GPSdata['date'][0:5] + ' ' + GPSdata['time'], 0, 0)
            
        
    # visulise the display text on the OLED
    display.show()



def is_leap_year(year):
    # Leap year rule: divisible by 4, but centuries must be divisible by 400
    # This matches the exact Gregorian calendar rule.
    
    #return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    if year % 400 == 0:
        # Divisible by 400 → leap year
        leap = True
    elif year % 100 == 0:
        # Divisible by 100 but not 400 → not a leap year
        leap = False
    elif year % 4 == 0:
        # Divisible by 4 but not 100 → leap year
        leap = True
    else:
        # All other years → not a leap year
        leap = False

    if leap:
        return 1
    else:
        return 0



# in micropython/python all fn parameters are inputs, return outputs
# with return statement
def UTCtoLocalDateAndTime(utcTime, utcDate, utcOffset):

        # utcTime="054946.000", utcDate="090825"
        # print(f"utcTime={utcTime}, utcDate={utcDate}, utcOffset={utcOffset}")

        # Convert the UTC time from the NMEA sentence into local time.
        # This  code  caters  for  positive and  negative  UTC  offest
        # values.   It  does not  cater  for  partial hours,  that  is
        # minutes.  Where UTC offset is a float value.
    

        # Convert all  the NMEA string  data into integers  for easier
        # calculations, then reconstruct the string at the end.
    
        # Extract year from UTC date (format: DDMMYY), prepend '20'
        # for full year (e.g., '25' → '2025')
        year = 2000 + int(utcDate[4:])
        # Extract month from UTC date (e.g., '01' for January)
        month = int(utcDate[2:4])
        # Extract day from UTC date (e.g., '01' for 1st)
        day = int(utcDate[0:2])

        # Determine correct UTC offset for Sydney Australia.
        if isSydneyinDaylightSavingMode(year, month, day):
            utcOffset = 11  # AEDT
        else:
            utcOffset = 10  # AEST

        # UTC offset for Sydney based on the current date using the
        # known DST rules.

        # Sydney Daylight Saving Rules (as of 2025):
        # Starts: First Sunday in October
        # Ends: First Sunday in April
        # DST offset: UTC+11
        # Standard time: UTC+10

        # utcOffset as an integer = curUTCcOffsetSydneyAustralia()

        # Calculate hours by adding UTC offset to UTC hours, convert to string
        hour = int(utcTime[0:2]) + utcOffset
        # Extract minutes from UTC time (e.g., '34' from '013445.000')
        minute = int(utcTime[2:4])
        # Extract seconds from UTC time (e.g., '45' from '013445.000')
        second = int(utcTime[4:6])


        # Now correct for positive and negative utcOffset, leap years
        # and day/month/year rollovers.

        # Maximum Days in each month (adjust February for leap year) ---
        monthDays = [31, 28 + is_leap_year(year), 31, 30, 31, 30,
                      31, 31, 30, 31, 30, 31]

        # --- 4. Adjust forward in time if hour >= 24 ---
        while hour >= 24:
            hour -= 24
            day += 1
            # If day goes past the end of the month → move to next month
            if day > monthDays[month - 1]:
                day = 1
                month += 1
                # If month goes past December → move to January of next year
                if month > 12:
                    month = 1
                    year += 1
                # Update February days for new year
                monthDays[1] = 28 + is_leap_year(year)

         
        # --- 5. Adjust backward in time if hour < 0 ---
        while hour < 0:
            hour += 24
            day -= 1
            # If day goes before the start of the month → move to
            # previous month
            if day < 1:
                month -= 1
                # If month goes before January → move to December of
                # previous year
                if month < 1:
                    month = 12
                    year -= 1
                # Update February days for new year
                monthDays[1] = 28 + is_leap_year(year)
                # Set day to last day of the new month
                day = monthDays[month - 1]
                

         # --- 6. Format date/time strings with leading zeros if necessary ---
        time = f"{hour:02d}:{minute:02d}:{second:02d}" # "03:07:05"
        date = f"{day:02d}/{month:02d}/{year}"         #"09/08/2025"      
        # f"..." → f-string syntax; lets you put variables directly inside {}.
        # {hour:02d} → format specifier:
        # 02 → pad the number with zeros so it’s at least 2 digits wide.
        # d → treat the value as an integer (decimal).
        # The result will always be two digits, e.g.:
        # 3 → "03"
        # 15 → "15"
        # So if hour = 3, minute = 7, second = 5,
        # time will be "03:07:05".

        # However, older C style method is still widely used
        # time = "%02d:%02d:%02d" % (hour, minute, second)
        

        # Combine hours, minutes, seconds into time string (e.g., '20:34:45')
        #time = hour + ':' + minute + ':' + second
        # Combine month, day, year into date string (e.g., '12/31/2024')
        #date = day + '/' + month + '/' + year

        return time, date



###############################################################################
#                                   main.cpp                                  #
###############################################################################


butOnePin = 12 # button one is connected to GPIO pin 12
butOne = Pin(butOnePin, Pin.IN, Pin.PULL_UP) # object associated GPIO pin 12
butOneUp = 0 # button goes down to up
butOneDown = 0# button goes up to down
butOneOld = 1 # last time through the loop the buttion was up
 
screenOne = True # display screen one fist
 
def butOneIRQ(pin):
    global butOneUp,butOneDown
    global butOneOld #previous state of button
    global screenOne
    butOneValue = butOne.value() # member function of butOne object
    #print("butOneValue", butOneValue)

    # denouncing the switch
    #
    if butOneValue==0:
        butOneDown = time.ticks_ms() # time when button pressed down
    else:
        butOneValue==1
        butOneUp = time.ticks_ms() # time when button goes back up

    # If in the last loop the button was in the up state and is now
    # pressed down in this loop, with a 50ms hysteresis(for switch
    # debounce noise, eg may get multiple 0's before you get a 1 and
    # visa versa).  Also, obviously button is pressed down after it was
    # in the up state last so butOneDown-butOneUp is a +ve value.
    if (butOneOld==1) and (butOneValue==0) and ((butOneDown-butOneUp) > 50):
        # This is atomic for simple assignments like booleans in
        # mycropython.  Counters, lists, dicts, multi-step operations:
        # use disable_irq() or carefully designed atomic methods.
        screenOne = not screenOne
        print('Button One Triggered')
    butOneOld=butOneValue

############################################################################
# irq's are seperate threads in mycropython, they are preemptive
#
############################################################################

# button going from 1 to 0, call interrupt routine called butOneIRQ
# OR
# button going from 0 to 1, cal interrupt routine called butOneIRQ
butOne.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler = butOneIRQ)



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
            print("Time:", GPSdata['time'])
            print("Date:", GPSdata['date'])
            print("NumSattelites4fix: ", GPSdata['numSattelites4fix'])
            
            # we extract latitude and longitude in the format of
            # openstreetmap and google earth
            print("Latitude and Longitude: ",
            GPSdata['latitudeDecimalDegrees'],
            GPSdata['longitudeDecimalDegrees'])
            
            print("Knots: ", GPSdata['knots'])
            print("Heading: ", GPSdata['heading'])
            print("Geoid True Altitude:", GPSdata['trueAltitude'])
            print("GPS Ellipsoid Altitude:", GPSdata['altitude'])
            #print("Mag VarDir", GPSdata['Mag VarDir'])
            print()

        # Send the data to the sdd1306 OLED display.  That is write
        # the contents of the FrameBuffer to display memory
        displayOLED()
        time.sleep(1)
        
        # NOTE: this does not overflow the buffer as readGPSdata()
        # executes in another thread.
        # time.sleep(10)


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

    # blank the OLED screen, ready for next display output
    display.fill(0)
    display.show()

    print("Exited Cleanly")
     
    
