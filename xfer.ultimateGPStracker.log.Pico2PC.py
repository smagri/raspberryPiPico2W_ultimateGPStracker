# Python command line program to xfer logfiles/files flashed to the
# Pico W to PC.

import serial
import time


serialPort= "/dev/ttyACM0"
baudRate = 115200 # for the pico it dosen't seem you can change this baudRate


# Open serial port connection to the pico.

# If this script doesn't get a response from the pico within 5 seconds
# it times out  and continues with the program,  hence timout=5.  Here
# serialObj  is  the  handle  for  our  serial  port.   For  instance,
# readline() operation  will wait  at most 5  seconds for  data before
# giving up.
serialObj = serial.Serial(serialPort, baudRate, timeout=5)
# To give the UART/hardware and python script time to connect to each
# other.
time.sleep(1)


# So you  don't need to unplug  and plug the pico  between writing the
# logfile and trying to run this  file.  The plug unplug works because
# it closes  and open file  handles, clears the  REPL state(micopython
# state, or interactive prompt >>>)  and reinitialises the USB serial.
# Note I'm  assuming the  filePicoHandle.close() has  already occured,
# otherwise you need to add that to your code.

# serialObj.write(b'\x03')  # Ctrl-C: break any running code
# time.sleep(1)
# serialObj.write(b'\x04')  # Ctrl-D: soft reset
# time.sleep(1)

# Stop any running code
# serialObj.write(b'\x03')  # Ctrl-C
# time.sleep(0.1)
# serialObj.reset_input_buffer()

# # Soft reset
# serialObj.write(b'\x04')  # Ctrl-D
# time.sleep(1)


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

# \r\n are  required by  MicoPython REPL  on the  pico. \r  is carrige
# return and  \n is linfeed/newline.   So together \r\n is  a standard
# EOL sequence used in many communication protocols, especially serial
# terminals.

# The MicroPython REPL(mycropython running on the pico essentially) is
# the interactive prompt that lets you talk directly to a board (like
# the Raspberry Pi Pico or ESP32) running MicroPython. >>> is the REPL
# prompt, waiting for your python code.

# REPL stands for Read–Eval–Print Loop:
# Read → It reads what you type in (a Python command).
# Eval → It evaluates (executes) that command on the microcontroller.
# Print → It prints the result back to you.
#Loop → Then it waits for the next command.

# .write()  method expects  raw bytes  to send  over the  serial port.
# Computers  and microcontrollers  communicate  via  bytes not  python
# string objects.
serialObj.write(b"filePicoHandle=open('ultimateGPStracker.log','r')\r\n")

# After  the pico  recived the  write() command  it returns/echos  the
# command back to the PC, so we can read it in.

#.decode('utf-8') converts the bytes receive from serial into a string.
# So, Latitude,Longitude becomes "Latitude,Longitude"???

# .strip() removes and leading and trailing whitespace charcters from
# the string, including \r\n
picoCmdResultLine = serialObj.readline().decode('utf-8').strip()
###print(picoCmdResultLine)
time.sleep(1)

# Reading from logfile logfile on the pico to logfile on the PC:

# PC logfile opened and filePChandle is the program handle to it.
with open('ultimateGPStracker.log.OnPC.log', 'w') as filePChandle:

    # Read all the lines of the pico logfile till there are no lines.
    # That is EOF is an empty STRING(hence, double quotes).
    while picoCmdResultLine != "''":

        # Write   a  line   to   the  pico   which   echos  the   sent
        # command(readline())to  the  PC  and  actually  executes  the
        # command on the  pico.  The command is to read  the next line
        # in the logfile.
        serialObj.write(b"filePicoHandle.readline()\r\n")

        # Read the echo of the readline() command.

        #.decode('utf-8') converts the bytes received from serial port
        # into    a    string.

        # .strip() removes and leading and trailing whitespace charcters from
        # the string, including \r\n

        # .readline() method blocks waiting from data from the pico or
        # untill the timout.
        echoLine = serialObj.readline().decode('utf-8').strip()
        if not echoLine:
            print("No echo recived from pico, timout hit. Breaking...")
            break
        ###print("Echo Line: ", echoLine)

        # Read the lines of the pico logfile
        picoCmdResultLine = serialObj.readline().decode('utf-8').strip()
        if not picoCmdResultLine:
            print("No data received from pico, timout hit. Breaking..")
            break
        ###print("File line: ", picoCmdResultLine)
        
        
        # Write what is  in the logfile on the pico into  the logfile on
        # the PC.
        if picoCmdResultLine.startswith("'") and picoCmdResultLine != "''":
            # Write lines starting with ' but not the blank line ''
            
            # The  Pico   sends  lines   as  string   literals,  e.g.,
            # '-33.77654,150.9693\n'.   The  code  removes  the  extra
            # quotes and  newline: [1:-3] → starts  from 2nd character
            # to 3rd-from-last  (removes leading ' and  trailing \n').
            # Writes the  cleaned line  to the PC  log file,  adding a
            # newline for proper formatting.
            #
            # This removes the \, n, ' ie three characters.
            picoCmdResultLine = picoCmdResultLine[1:-3]
            # newline to have each line under the other instead of side by side
            ###print("Pico File Line read in is=", picoCmdResultLine)
            filePChandle.write(picoCmdResultLine + '\n')

# close the log file on the pico
serialObj.write(b"filePicoHandle.close()\r\n")
# close the serial port connection from the PC to the pico.
serialObj.close()
