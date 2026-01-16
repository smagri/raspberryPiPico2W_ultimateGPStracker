#!/usr/bin/env python3

# Transfer sdcard  logfile to  PC.  Then convert  this logfile  to kml
# format for googleEarth and other such systems.

# Refer to cd docs; less README.sdcardControlLinks

# Firstly:

###############################################################################
# Python command line program to xfer logfiles/files from from sdcard to PC.
#
###############################################################################

# Setup SPI comms with the sdcard
spi = SPI(1,sck=Pin(14), mosi=Pin(15), miso=Pin(12))
#cs = Pin(13)
cs = Pin(13, Pin.OUT) # by default this is an input pin
try:
    moduleSDcard = sdcard.SDCard(spi, cs)
    print("SDCard init OK")
except Exception as e:
    print("SDCard init FAILED:", e)
    return None, None

#print("dbg: main: MOUNT sdcard")
#os.mkdir('/sd')

# Mount the sdcard on your PC filesystem, ready for creating and
# accessing files on it like any other file on your PC.
os.mount(moduleSDcard, '/sd')

# Open logfile on the sdcard for reading
print("\nOPENING sdcard logfile")

sdcard_file_handle = open('/sd/ultimateGPStrackerSDcard.log', 'r')


# The logfile ma be large so I prefer reading and writing in chunks,
# read() loads the whole file into memory/RAM

#sdcard_file_data = sdcard_file_handle.read()
#sdcard_file_handle.close()

# Write the file data to a file on the PC

# Open the file for writing on your PC.
with open("ultimateGPStrackerSDcard.log.onPC.log", encoding="utf-8", mode="w") as pc_logfile_handle:
    for line in sdcard_file_handle:
        pc_logfile_handle.write(line)
    

# open()  out of  scope  so  sdcard logfile  copied  to  PC is  closed
# automatically, as  used with open instead  of just open to  open the
# file

print(f"Logfile copied to PC as: ultimateGPStrackerSDcard.log.onPC.log")

# Close the sdcard logfile as it was not opened with, with open
print("\nClosing logfile on sdcard")
sdcard_file_handle.close()

print("\nUnmounting SDcard")
os.umount("/sd")
        
print("\nExited Cleanly")



# ###############################################################################
# #                     Convert PC cvs logfile to kml format.
# ###############################################################################

# kml_waypoints = ""
# kml_waypoints_path = ""
# cvs_file = "ultimateGPStracker.log.OnPC.log"

# with open(cvs_file, 'r', encoding='utf-8') as filePChandle:
#     # for loop automatically stops at EOF.
#     #
#     # Each time through the loop, line is assigned the next line of text
#     # (including its  trailing \n).  When  there are no more  lines, the
#     # iterator  raises a  StopIteration signal  internally.  So  the for
#     # loop catches that automatically and exits cleanly.
#     for line in filePChandle:
#         # remove all leading and trailing whitespace(spaces,tabs,and
#         # newlines) from the line just read.
#         line = line.strip()
#         if not line:
#             # skip over blank lines
#             continue

#         # splits the stirng in two parts at the , delimiter
#         latitude, longitude = line.split(',')


#         # <Point><coordinates>\n{longitude},{latitude}\n</coordinates></Point>\n"
#         # Sets up the waypoints.

#         #  <altitudeMode>clampToGround</altitudeMode>   is   used   so
#         #  elevation is not  taken into account for  the waypoints, as
#         #  otherwise  we may  loose display  of some  waypoints.  Your
#         #  waypoints may disappear  due to some error  in the elevation
#         #  of your waypoints.

#         # kml_waypoints_path connects all the waypoints with a red(setup
#         # in  header)   line  path.  Note  that   google  earth  expects
#         # longitude,latitude<space>.
        
#         # f-strings(formatted string  literal) lets you  embed VARIABLES
#         # or expressions directly inside a  string, using {} braces.  It
#         # automatically converts numbers to strings.  Cleaner than using
#         # plus sign to concatinate strings with variables in them.
        
#         kml_waypoints += f"<Point><coordinates>\n{longitude},{latitude}\n</coordinates></Point>\n"
#         kml_waypoints_path += f"{longitude},{latitude} \n"

#         # {kml_waypoints_path} the f  string kml_waypoints_path needs to
#         # be put  within braces  as it  is already  within an  f string.
#         # Otherwise, literally  kml_waypoints_path as a string  would be
#         # printed in the kml_content.

#         # Some other notes on f strings:
#         # f-strings are evaluated at the time the string is created.
#         # Anything inside {} is evaluated as an expression.
#         # Anything outside {} is just literal text.

#         # if you weren’t using an f-string, you could also do:

#         # Pauth essentially did this:
#         # kml_path_footer = """
#         # <coordinates>
#         # """ + kml_waypoints_path + """
#         # </coordinates>
#         # """

#         # But f  strings are cleaner  and more readable,  especially for
#         # multi-line text like KML

#         #######################################################################
#         # SUMMARY f-string:
#         #
#         # The  curly  braces {}  are  only  needed around  variables  or
#         # expressions whose  values you want inserted  into an f-string.
#         # Everything  else outside  the braces  is just  plain text.  It
#         # looks     after     changing     variables     to     strings.
#         # ######################################################################
        
        
# # ### Triple quotes  allow you to write multiline  strings, that include
# # spaces, indentation and newlines.

# # kml  path header  sets  the name  of the  file  name(Path from  Pico).
# # Waypoints  style(black  point,   or  palcemark_circle.png).   And  the
# # Placemark  line  sytle(red   path).   <MultiGeometry  </MultiGeometry>
# # indicate that  multiple points/waypoints on  the path are going  to be
# # added to this section.

# # NOTE: for a kml  file there is always a pair  to Opening and Closing
# # markers.  eg <Placemark> and </Placemark>.

# kml_file_content = f"""<?xml version="1.0" encoding="UTF-8"?>
# <kml xmlns="http://www.opengis.net/kml/2.2">
#   <Document>
#     <name>Path from Pico</name>
#     <Style id="pointStyle">
#       <IconStyle>
#         <Icon><href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href></Icon>
#         <scale>1.0</scale>
#       </IconStyle>
#     </Style>
#     <Style id="lineStyle">
#       <LineStyle><color>ff0000ff</color><width>3</width></LineStyle>
#     </Style>
#     <Placemark>
#       <styleUrl>#pointStyle</styleUrl>
#       <MultiGeometry>
#       {kml_waypoints}
#       </MultiGeometry>
#     </Placemark>
#     <Placemark>
#       <name>Path</name>
#       <styleUrl>#lineStyle</styleUrl>
#       <LineString>
#         <tessellate>1</tessellate>
#         <altitudeMode>clampToGround</altitudeMode>
#         <coordinates>
#         {kml_waypoints_path}
#         </coordinates>
#       </LineString>
#     </Placemark>
#   </Document>
# </kml>
# """

# kml_file = "ultimateGPStracker.log.OnPC.log.kml"

# with open(kml_file, 'w', encoding='utf-8') as filePChandle:
#     filePChandle.write(kml_file_content)

# # again we have a string kml_file inside a string so we need {}
# print(f"KML file {kml_file} created successfully.")

# # This will still work but is less clean code
# #print("KML file " + kml_file + " created successfully.")

    
