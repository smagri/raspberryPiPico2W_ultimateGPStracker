19jul2025
updates:
26jul2025

This  project follows  Paul McWhorter  youtube videos  to build  a GPS
tracker with the Rasberry Pi Pico W.  However, I have used the Pi Pico
2 W and everything works well.

Bill of materials:
-----------------
Raspberry Pi Pico W: 
https://amzn.to/3FA4tqS

Adafruit Ultimate GPS version 3:
https://amzn.to/4jeRIjj

External Antenna (OPTIONAL) I would highly recommend this: 
https://amzn.to/4myFWTL

Button Battery For Quicker Fix: 
https://amzn.to/3FjoUbH

Breadvolt Power  Supply (OPTIONAL) I  would highly recommend  this for
when your project is finished:
https://amzn.to/4kuuJ50

Charging Cable (If You Don’t Have): 
https://amzn.to/3Z0EMGF

OLED SSD1306: 
https://amzn.to/43tFYUk

Soldering Iron: 
https://amzn.to/3HpZolw

Solder Practice Components:
https://amzn.to/4mNaEca

Extra Solder: 
https://amzn.to/4kuuDdE

Safety Glasses: 
https://amzn.to/4mwGMjR

Breadboard and Wires (If You Don’t Have): 
https://amzn.to/4kggv86


Programming the raspberry Pi Pico 2:
-----------------------------------

Raspberry Pi Pico 2 W with RP2350, is the correct firmware file from:
https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
mp_firmware_unofficial_latest.uf2

To flash firmware,  hold down bootsel button while  plugging in power,
then copy  .uf2 to  RP2350 mass  storage device  that appears  on your
computer.  If correctly flashed the  mass storage drive will dissapear
from your computer directory.

ls /dev/ttyACM0  should now  appear, so  select it  in thonny  and you
should get the miropython prompt.

Test with:
print("hello").

Why  use thonny  editor as  the default  editor for  rasberry pi  pico
projects:  I  use  emacs  for  editing  and  thonny  for  running  the
micropython scripts.
-------------------------------------------------------------------------

1.  Beginner-Friendly  Design:  Thonny is  specifically  designed  for
beginners in programming, especially  for Python. Its clean interface,
built-in debugger, and  minimal setup make it ideal for  new users and
education settings.

2.  Native Support  for MicroPython  The  Pico W  runs MicroPython,  a
lightweight version of Python for microcontrollers. Thonny has:

Built-in MicroPython support

A REPL (Read-Eval-Print Loop) interface to interact directly with the Pico

Automatic detection of MicroPython boards

This makes  it easy  to write,  upload, and  test code  on the  Pico W
without needing extra tools or command-line knowledge.


3. One-Click Installation & Setup
Setting up a Pico W with Thonny is simple:

Plug in the board (holding BOOTSEL)

Drag the firmware .uf2 file

Open Thonny, select the Pico interpreter (MicroPython on Raspberry Pi Pico)

Thonny handles the rest, including communication over USB serial.

4.  Thonny works  on Windows,  macOS,  and Linux  and is  lightweight,
requiring very few  resources. Perfect for use  on low-powered laptops
or in classrooms.

5. Official  Raspberry Pi Foundation Recommendation.  The Raspberry Pi
Foundation recommends Thonny  for Pico users in  its documentation and
tutorials  because  it aligns  with  their  goal of  making  computing
education accessible.


Alternatives Exist (for more advanced users)
While Thonny is ideal for beginners, advanced users sometimes prefer:

VS Code (with the Pico-Go extension)

mpremote + rshell for CLI tools

PyCharm (with some setup)


Installing the ssd1306.py, the ssd1306 driver for the OLED
----------------------------------------------------------

Get the current version of the ssd1306 driver from the github repository:

https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py

Copy it into the directory where your main.py file is, in our case
ultimateGPStracker.py is our main.py.

File->Save As and SELECT 'Raspberry Pi Pico' (not 'This Computer') to
write this driver into the pico's filesystem.
