Project started 19jul2025.

This  project follows  Paul McWhorter  youtube videos  to build  a GPS
tracker with the Rasberry Pi Pico W.  However, I have used the Pi Pico
2 W and everything works well.   Note also that all .pdf documents are
in  ~/proj/paulMcWhorter/docs/ultimateGPStracker also,  but links  are
given below.

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
-------------------------------------------------------------------------
projects:  I  use  emacs  for  editing  and  thonny  for  running  the
-------------------------------------------------------------------------
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

  * [ ] 
Alternatives Exist (for more anced users)
While Thonny is ideal for beginners, advanced users sometimes prefe:

VS Code (with the Pico-Go extension)

mpremote + rshell for CLI tools

PyCharm (with some setup)



Installing the ssd1306.py, the ssd1306 driver for the OLED
----------------------------------------------------------

Get the current version of the ssd1306 driver from the github repository:

From repository: https://github.com/micropython
https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py
In the directory:
https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306

Copy it into the directory where your main.py file is, in our case
ultimateGPStracker.py is our main.py.

File->Save As and SELECT 'Raspberry Pi Pico' (not 'This Computer') to
write this driver into the pico's filesystem.



Howto display on the ssd1306 OLED
---------------------------------
https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html



GPS - NMEA sentence information
-------------------------------
https://aprs.gids.nl/nmea/#rmc


CD-PA1616S GPS patch antenna module, ie for adafruit ultimate GPS version 3
---------------------------------------------------------------------------
Data Sheet V.04
---------------
https://cdn-shop.adafruit.com/product-files/746/CD+PA1616S+Datasheet.v03.pdf



Alternative method for calculating day and time(needs to be tested) in
----------------------------------------------------------------------
mycropython.
-----------
There is a function in the Pico that can do the heavy lifting for the
clock/calendar time offset, try this:

        utcDate = NMEAmain['GPRMC'].split(',')[9]
        myYear = int(utcDate[4:]) + 2000
        myMonth = int(utcDate[2:4])
        myDay = int(utcDate[0:2])

        utcTime = NMEAmain['GPGGA'].split(',')[1]
        myHours = int(utcTime[0:2])
        myMin = int(utcTime[2:4])
        mySec = int(utcTime[4:6])

        # Convert date/time to Epoch seconds, and add (/subtract) the offset in seconds
        myTimeDate = 
		time.mktime([myYear,myMonth,myDay,myHours,myMin,mySec,0,0]) + 3600 * utcCorrection
        
		# Convert Epoch time (now with the offset) back to date/time
        myYear,myMonth,myDay,myHours,myMin,mySec,myWday,myYday = time.gmtime(myTimeDate)

		# In some parts of the world, day and month are in reversed order.
		GPSdata['date'] = f'{myDay:2d}/{myMonth:02d}/{myYear:04d}' 
        GPSdata['time'] = f'{myHours:02d}:{myMin:02d}:{mySec:02d}'

Standard/summer time could be a flag that you set or reset manually,
during summertime you add an extra 3600 seconds to the Epoch time...



Thread yield, yield_thread() in readGPSdata() thread.
-----------------------------------------------------

We need to do this as there is a bug in the micropython implementation
on the  raspberry pi pico w  or pico 2  w hardware we are  using, when
doing threading.  See link to issue on the micropython github page.
https://github.com/micropython/micropython/issues/10621
https://github.com/micropython/micropython/issues/12698



PMTK command packets:
---------------------
https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf



Power Up using Bread Volt
-------------------------
* 3.3V rail to OLED VCC
* 5.0 rail to pin39 - VSYS
* copy ultimateGPStracker.py to main.py, as on power-up pico runs
  main.py automaticly
* if thonny doesn't find main.py due to symlink of lu1 just load it
  from the command line:

  thonny ultimateGPStracker.py main.py



Thonny hanging on File->Save As main.py and bug with hard reboot of
-------------------------------------------------------------------
system and using the Sunfounder Bread Volt.
-------------------------------------------------------------------

Firstly, my  rasberry pi  pico 2 w  is plugged into  the USB  port, no
Bread Volt attached.  Note it is a pico 2 w not a pico w.

Then I  started thonny, which does  a soft reboot of  the raspberry pi
pico 2  w on  startup, and  so my code  worked.  However,  with thonny
closed and  on a hard reboot(unplug  and replug in usb  cable) my code
did not work.

So I  tried to  flash main.py  via thonny File->Save  As and  it hung.
Consequently, I had  to execute the following commands  on the command
line to flash main.py into the raspberry pi pico 2 w:

Firstly, you will need these:
* pip install mpremote
* wget https://datasheets.raspberrypi.com/soft/flash_nuke.uf2

* with boot sel pressed plug in usb cable
* cp flash_nuke.uf2 /media/.../RP2350/ ,to clear mycropython from pico
* cp mp_firmware_unofficial_latest.uf2 /media/.../RP2350/ ,to copy
  back mycropython
* mpremote connect /dev/ttyACM0 fs ls ,should be empty
* mpremote connect /dev/ttyACM0 fs cp  main.py ssd1306 : ,to copy back
  your main file
* then your main.py is flashed to your pico
* mpremote connect /dev/ttyACM0 fs ls  ,should show main.py and
  ssd1306.py to be there.

However, this still didn't solve my problem with a hard reboot running
my code.  So then  I had to modify my code to fix  my bug.  Remember a
soft reboot,  running code from  thonny, the GPS receiver  had already
been  running  and my  code  worked.   So  I  guessed that  putting  a
time.sleep(10) in my main.py, after importing the libraries and before
any other  code, on a hard  reboot would give the  GPS receiver enough
time to settle before running any code.  Thus on a hard reboot my code
now worked.  Also, I was able to  unplug the pico from usb and use the
Bread Volt and everything worked fine.

Obviously, this is a hack but perhaps it would be fixed by polling the
GPS receiver via some register to see if it is actually up and running
before executing any  code.  Also, perhaps others are  not seeing this
problem as I am using a pico 2 w  not a pico w so the pico 2 is faster
so  perhaps is  not leaving  the GPS  receiver enough  time to  settle
properly before executing code.



Firmware(see firmware directory):
---------------------------------
flash_nuke.uf2

This is  a special erase utility  provided by Raspberry Pi.   When you
copy this  to your Pico  in BOOTSEL mode,  it erases the  entire flash
memory of the microcontroller.  Afterward,  the board will appear as a
blank device, and you can  install a fresh MicroPython, CircuitPython,
or C/C++  firmware.  It doesn’t  leave anything  useful to run  – it’s
purely for “factory reset” of the flash.


mp_firmware_unofficial_latest.uf2

This is  a firmware image  containing MicroPython (MP  = MicroPython).
"Unofficial"  means  it’s  not  from  the  Raspberry  Pi  foundation’s
official builds but  probably from a community  contributor or nightly
build.  Copying this  .uf2 onto the Pico in BOOTSEL  mode will install
MicroPython on the device.

After flashing, the Pico will reboot and expose a REPL (interactive
Python shell) over USB.

In short:

* .uf2 = a firmware update file format.
* flash_nuke.uf2 = erases the chip.
* mp_firmware_unofficial_latest.uf2 = installs MicroPython firmware.
