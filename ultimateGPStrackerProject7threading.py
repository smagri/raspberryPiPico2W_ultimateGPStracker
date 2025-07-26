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

# this is a python dictionary, like an array in c and c++
# index=GPGGA, data=="" at this stage
NMEAdata = {
    'GPGGA' : "",
    'GPGSA' : "",
    'GPRMC' : "",
    'GPVTG' : ""
    }



def gpsThread():
    print("Thread Running")
    global keepRunning, NMEAdata
    # string key will have data from NMEAdata strings in dictionary
    GPGGA = ""
    GPGSA = ""
    GPRMC = ""
    GPVTG = ""
    while not GPS.any():
        # no data in buffer
        pass
    # we have data in buffer
    while GPS.any():
        # read from buffer which clears the buffer,
        # then print the junk
        junk = GPS.read()
        print(junk)
        myNMEA = "" # clear the NMEA container string
    while keepRunning:
        if GPS.any():
            # read each myNEMA sensce string line to EOL
            myChar=GPS.read(1).decode('utf-8')
            myNMEA+=myChar
            if myChar == '\n':
                myNMEA = myNMEA.strip()
                # store the NMEAdata into the dictionary
                if myNMEA[1:6] == "GPGGA":
                    GPGGA = myNMEA
                if myNMEA[1:6] == "GPGSA":
                    GPGSA = myNMEA
                if myNMEA[1:6] == "GPRMC":
                    GPRMC = myNMEA
                if myNMEA[1:6] == "GPVTG":
                    GPVTG = myNMEA
                # we update the dictionary only when data in all 4 NMEAdata is full
                if GPGGA != "" and GPGSA!="" and GPRMC!="" and GPVTG!="":
                    # so main thread doesn't mess with our NMEAdata we
                    # update the dictionary safely with the mutex lock
                    dataLock.acquire()
                    NMEAdata = {
                        'GPGGA' : GPGGA,
                        'GPGSA' : GPGSA,
                        'GPRMC' : GPRMC,
                        'GPVTG' : GPVTG
                        } # dictionary update done
                    dataLock.release()
                # reset myNMEA for next itteration
                myNMEA = ""
    print("Thread Terminated Cleanly")


_thread.start_new_thread(gpsThread,())
#time.sleep(2)
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    # kill thread first before GPS board to exit cleanly
    keepRunning = False
#    time.sleep(1)
    GPS.deinit()
#    time.sleep(1)
    print("Exited Cleanly")
    