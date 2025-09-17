from machine import Pin,I2C,UART
import time
import _thread
from ssd1306 import SSD1306_I2C
import math

utcCorrect = 3
earthRadius = 6371000
i2c2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
dsp = SSD1306_I2C(128,64,i2c2)

sysState = 0

dataLock = _thread.allocate_lock()
keepRunning = True
GPS = UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
# Reset GPS
GPS.write(b'$PMTK314,-1*04\r\n')
#The following line ensures that the GPS reports the GPVTG NMEA Sentence
GPS.write(b"$PMTK314,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n")
NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
    }
GPSdata = {
    'latDD' 	: 0,
    'lonDD'		: 0,
    'heading'	: 0,
    'fix'		: False,
    'sats'		: 0,
    'knots'		: 0,
    'time'		: '00:00:00',
    'date'		: '00/00/0000',
    'alt'		: 0.0
    }
def calculateDistance(lat1,lon1,lat2,lon2):
    lat1=lat1*2*math.pi/360
    lon1=lon1*2*math.pi/360
    lat2=lat2*2*math.pi/360
    lon2=lon2*2*math.pi/360
    theta = 2*math.asin(math.sqrt(
        math.sin((lat2-lat1)/2)**2 +
        math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
        ))
    distance = earthRadius * theta
    return distance
def calculateHeading(lat1,lon1,lat2,lon2):
    lat1=lat1*2*math.pi/360
    lon1=lon1*2*math.pi/360
    lat2=lat2*2*math.pi/360
    lon2=lon2*2*math.pi/360
    deltaLon=lon2-lon1
    xC=math.sin(deltaLon)*math.cos(lat2)
    yC=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(deltaLon)
    beta = math.atan2(xC,yC)
    betaDeg = beta*360/2/math.pi
    return betaDeg
def gpsThread():
    print("Thread Running")
    global keepRunning,NMEAdata
    GPGGA = ""
    GPGSA = ""
    GPRMC = ""
    GPVTG = ""
    while not GPS.any():
        pass
    while GPS.any():
        junk = GPS.read()
        print(junk)
    myNMEA = ""
    while keepRunning:
        if GPS.any():
            myChar=GPS.read(1).decode('utf-8')
            myNMEA = myNMEA + myChar
            if myChar == '\n':
                myNMEA = myNMEA.strip()
                if myNMEA[1:6] == "GPGGA":
                    GPGGA = myNMEA
                if myNMEA[1:6] == "GPGSA":
                    GPGSA = myNMEA
                if myNMEA[1:6] == "GPRMC":
                    GPRMC = myNMEA
                if myNMEA[1:6] == "GPVTG":
                    GPVTG = myNMEA
                if GPGGA != "" and GPGSA!="" and GPRMC!="" and GPVTG!="":
                    dataLock.acquire()
                    NMEAdata = {
                        'GPGGA' : GPGGA,
                        'GPGSA' : GPGSA,
                        'GPRMC' : GPRMC,
                        'GPVTG' : GPVTG
                        }
                    dataLock.release()
                myNMEA = ""
    print("Thread Terminated Cleanly")
def parseGPS():
    readFix=int(NMEAmain['GPGGA'].split(',')[6])
    if readFix !=0:
        GPSdata['fix'] = True
        latRAW = NMEAmain['GPGGA'].split(',')[2]
        latDD = int(latRAW[0:2]) + float(latRAW[2:])/60
        if NMEAmain['GPGGA'].split(',')[3] == 'S':
            latDD = -latDD
        GPSdata['latDD']= latDD
        lonRAW=NMEAmain['GPGGA'].split(',')[4]
        lonDD=int(lonRAW[0:3]) + float(lonRAW[3:])/60
        if NMEAmain['GPGGA'].split(',')[5] == 'W':
            lonDD = -lonDD
        GPSdata['lonDD'] = lonDD
        heading = float(NMEAmain['GPRMC'].split(',')[8])
        GPSdata['heading'] = heading
        knots = float(NMEAmain['GPRMC'].split(',')[7])
        GPSdata['knots'] = knots
        sats = int(NMEAmain['GPGGA'].split(',')[7])
        GPSdata['sats'] = sats
        utcTime = NMEAmain['GPGGA'].split(',')[1]
        utcDate = NMEAmain['GPRMC'].split(',')[9]
        # utcTime = "013445.000"
        # utcDate = "010125"

        # Extract year from UTC date (format: DDMMYY), prepend '20' for full year (e.g., '25' → '2025')
        myYear = '20' + utcDate[4:]
        # Extract month from UTC date (e.g., '01' for January)
        myMonth = utcDate[2:4]
        # Extract day from UTC date (e.g., '01' for 1st)
        myDay = utcDate[0:2]
        # Calculate hours by adding UTC offset to UTC hours, convert to string
        myHours = str(int(utcTime[0:2]) + utcCorrect)
        # Extract minutes from UTC time (e.g., '34' from '013445.000')
        myMin = utcTime[2:4]
        # Extract seconds from UTC time (e.g., '45' from '013445.000')
        mySec = utcTime[4:6]

        # Define array of maximum days per month (index 0-11 for months 1-12: Jan to Dec)
        maxDays = ['31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']

        # Check if year is a leap year (simplified: divisible by 4); if so, set February to 29 days
        if int(myYear) % 4 == 0:
            maxDays[1] = '29'

        # Check if hours exceed 24 (for positive UTC offsets, e.g., UTC 22:00 + 5 = 27:00)
        if int(myHours) >= 24:
            # Subtract 24 from hours to wrap around to next day (e.g., 27 → 3)
            myHours = str(int(myHours) - 24)
            # Pad hours with leading zero if single digit (e.g., '3' → '03')
            if len(myHours) < 2:
                myHours = '0' + myHours
            # Increment day to account for crossing midnight (e.g., 30 → 31)
            myDay = str(int(myDay) + 1)
            # Check if day exceeds maximum days for the current month (e.g., June 31 > 30)
            if int(myDay) > int(maxDays[int(myMonth) - 1]):
                # Reset day to 1 for the next month
                myDay = '01'
                # Increment month (e.g., June → July)
                myMonth = str(int(myMonth) + 1)
                # Check if month exceeds 12 (e.g., December → January)
                if int(myMonth) > 12:
                    # Reset month to January
                    myMonth = '01'
                    # Increment year (e.g., 2025 → 2026)
                    myYear = str(int(myYear) + 1)
            # Pad day with leading zero if single digit (e.g., '1' → '01')
            if len(myDay) < 2:
                myDay = '0' + myDay
            # Pad month with leading zero if single digit (e.g., '7' → '07')
            if len(myMonth) < 2:
                myMonth = '0' + myMonth

        # Check if hours are negative (for negative UTC offsets, e.g., UTC 01:00 - 5 = -4)
        if int(myHours) < 0:
            # Add 24 to hours to wrap around to previous day (e.g., -4 → 20)
            myHours = str(int(myHours) + 24)
            # Pad hours with leading zero if single digit (e.g., '3' → '03')
            if len(myHours) < 2:
                myHours = '0' + myHours
            # Decrement day to account for crossing midnight backward (e.g., 01 → 00)
            myDay = str(int(myDay) - 1)
            # Check if day is less than 1 (e.g., January 1 → December 31)
            if int(myDay) < 1:
                # Decrement month (e.g., January → December)
                myMonth = str(int(myMonth) - 1)
                # Check if month is less than 1 (e.g., January → December of previous year)
                if int(myMonth) < 1:
                    # Set month to December
                    myMonth = '12'
                    # Decrement year (e.g., 2025 → 2024)
                    myYear = str(int(myYear) - 1)
                # Set day to maximum days of the new month (e.g., December → 31)
                myDay = maxDays[int(myMonth) - 1]
            # Pad day with leading zero if single digit (e.g., '1' → '01')
            if len(myDay) < 2:
                myDay = '0' + myDay
            # Pad month with leading zero if single digit (e.g., '7' → '07')
            if len(myMonth) < 2:
                myMonth = '0' + myMonth

        # Combine hours, minutes, seconds into time string (e.g., '20:34:45')
        myTime = myHours + ':' + myMin + ':' + mySec
        # Combine month, day, year into date string (e.g., '12/31/2024')
        myDate = myMonth + '/' + myDay + '/' + myYear
        # Store local time in GPSdata dictionary
        GPSdata['time'] = myTime
        # Store local date in GPSdata dictionary
        GPSdata['date'] = myDate
        GPSdata['alt'] = float(NMEAmain['GPGGA'].split(',')[9])
def dispOLED():
    global sysState,latitude1,longitude1,latitude2,longitude2
    dsp.fill(0)
    if GPSdata['fix'] == False:
        dsp.text("Waiting for Fix . . .",0,0)
    if GPSdata['fix'] == True:
        if sysState%5== 0:
            dsp.fill(0)
            dsp.text("Ultimate GPS",0,0)
            dsp.text(GPSdata['date'][0:5] + ' '+GPSdata['time'],0,16)
            dsp.text("LAT: "+str(GPSdata['latDD']),0,26)
            dsp.text("LON: "+str(GPSdata['lonDD']),0,36)
            dsp.text("SATS: "+str(GPSdata['sats']),0,46)

        if sysState%5==1:
            latitude1=GPSdata['latDD']
            longitude1=GPSdata['lonDD']
            sysState = 2
        if sysState%5==2:
            dsp.fill(0)
            dsp.text("Ultimate GPS",0,0)
            dsp.text(GPSdata['date'][0:5] + ' '+GPSdata['time'],0,16)
            dsp.text("P1 lat "+str(latitude1),0,26)
            dsp.text("P1 lon "+str(longitude1),0,36)
            dsp.text("Proceed to P2",0,46)
            dsp.text("Then Press Btn",0,56)
        if sysState%5==3:
            latitude2=GPSdata['latDD']
            longitude2=GPSdata['lonDD']
            sysState=4
        if sysState%5==4:
            dsp.fill(0)
            dsp.text("Ultimate GPS",0,0)
            dsp.text(GPSdata['date'][0:5] + ' '+GPSdata['time'],0,16)
            dist=calculateDistance(latitude1,longitude1,latitude2,longitude2)
            head=calculateHeading(latitude1,longitude1,latitude2,longitude2)
            dsp.text("Dist: "+str(dist),0,26)
            dsp.text("Head: "+str(head),0,36)
    dsp.show()
butOnePin = 12
butOne = Pin(butOnePin, Pin.IN, Pin.PULL_UP)
butOneUp = 0
butOneDown = 0
butOneOld = 1

def butOneIRQ(pin):
    global butOneUp,butOneDown,butOneOld,sysState
    butOneValue = butOne.value()
    if butOneValue==0:
        butOneDown=time.ticks_ms()
    if butOneValue==1:
        butOneUp = time.ticks_ms()
    if butOneOld==1 and butOneValue==0 and butOneDown-butOneUp>50:
        sysState = sysState + 1
        print('Button One Triggered')
    butOneOld=butOneValue
    
butOne.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING , handler = butOneIRQ)
 
_thread.start_new_thread(gpsThread,())
time.sleep(3)
try:
    while True:
        dataLock.acquire()
        NMEAmain = NMEAdata.copy()
        dataLock.release()
        parseGPS()
        if GPSdata['fix'] == False:
            print("Waiting for Fix . . .")
        if GPSdata['fix'] == True:
            print("Ultimate GPS Tracker Report: ")
            print(GPSdata['time'],GPSdata['date'])
            print("Lat and Lon: ",GPSdata['latDD'],GPSdata['lonDD'])
            print("Knots: ",GPSdata['knots'])
            print("Heading: ",GPSdata['heading'])
            print("Elevation: ",GPSdata['alt'])
            print("Sats: ",GPSdata['sats'])
            print()
        dispOLED()
        time.sleep(1)


except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    keepRunning = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    dsp.fill(0)
    dsp.show()
    print("Exited Cleanly")
