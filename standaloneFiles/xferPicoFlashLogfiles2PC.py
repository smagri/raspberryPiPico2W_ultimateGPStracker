#!/usr/bin/env python3

# Python command line program to xfer logfiles/files flashed to the
# Pico W to PC.

import serial
import time

serialPort= "/dev/ttyACM0"
baudRate = 115200 # for the pico it dosen't seem you can change this baudRate

# If this script doesn't get a response from the pico within 5 seconds
# it times out  and continues with the program,  hence timout=5.  Here
# serialObj is the handle for our serial port.
serialObj = serial.Serial(serialPort, baudRate, timeout=5)
# To give the UART/hardware and python script time to connect to each
# other.
time.sleep(1)

# The pico is really the system that xfers the data to this python
# script running on the PC.  So we need to send commands to the pico
# as follows.

# An example of opening the pico logfile and reading the echoed
# response:

# Send bytes,  b, to  the pico,  open the  log file  on the  pico with
# handle filePicoHandle.   'with' keyword  handled opening  an closing
# the file  in our last  lession but here  because we are  running two
# machines, the  pico and the PC.   CR and LF are  required instead of
# doing it manually.
serialObj.write(b"filePicoHandle=open('logOnPico.txt','r')\r\n")

# After  the pico  recived the  write() command  it returns/echos  the
# command back to the PC, so we can read it in.

# .strip() removes and leading and trailing whitespace charcters from
# the string.
picoCmdResultLine =serialObj.readline().decode('utf-8').strip()
print(picoCmdResultLine)
time.sleep(1)

# Reading from logfile logPico.txt on the pico to logPC.txt on the PC:

# PC logfile opened if filePChandle handle
with open('logOnPC.txt','w') as filePChandle:

    # Read all the lines of the pico logfile till there are no lines.
    # That is EOL/EOF is an empty STRING(hence, double quotes).
    while picoCmdResultLine != "''":

        # Write   a   line   to   the    pico   which   echos   the   sent
        # command(readline())to the  PC and actually executes  the command
        # on the pico.
        serialObj.write(b"filePicoHandle.readline()\r\n")

        # Read the echo of the readline() command
        echoLine = serialObj.readline().decode('utf-8').strip()
        #time.sleep(0.01)
        #print("Echo Line: ", echoLine)
        # Read the lines of the logPico.txt logfile
        picoCmdResultLine =serialObj.readline().decode('utf-8').strip()
        #print("File line: ", picoCmdResultLine)
        
        
        # Write what is  in the logOnPico.txt logfile into  the logfile on
        # the PC, logOnPC.txt
        if picoCmdResultLine.startswith("'") and picoCmdResultLine != "''":
            # Write lines starting with ' but not the blank line ''
            
            #         line =serialObj.readline().decode('utf-8').strip()
     #         print("LINE: ",line)
     #         if line.startswith("'") and line !="''":
            # pick char 1 and remove last three
            picoCmdResultLine = picoCmdResultLine[1:-3]
            # newline to have each line under the other instead of side by side
            print("Pico File Line read in is=", picoCmdResultLine)
            filePChandle.write(picoCmdResultLine + '\n')

# close the log file on the pico
serialObj.write(b"filePicoHandle.close()\r\n")
# close the serial port connection from the PC to the pico.
serialObj.close()
