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


try:
    
except KeyboardInterrupt:
    print("\nStopping Program . . . Cleaning Up UART")
    keepRunning = False
    time.sleep(1)
    GPS.deinit()
    time.sleep(1)
    print("Exited Cleanly")
