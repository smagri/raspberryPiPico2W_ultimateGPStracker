from machine import Pin,I2C,UART
import time
import _thread
dataLock = _thread.allocate_lock()
keepRunning = True
GPS = UART(1, baudrate=9600, tx=machine.Pin(8), rx=machine.Pin(9))
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
    'knots'		: 0
    }
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
        sats = NMEAmain['GPGGA'].split(',')[7]
        GPSdata['sats'] = sats
        
        
_thread.start_new_thread(gpsThread,())
time.sleep(2)
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
            print("Lat and Lon: ",GPSdata['latDD'],GPSdata['lonDD'])
            print("Knots: ",GPSdata['knots'])
            print("Heading: ",GPSdata['heading'])
            print("Sats: ",GPSdata['sats'])
            print()

        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    keepRunning = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    print("Exited Cleanly")
