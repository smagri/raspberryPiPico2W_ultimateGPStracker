# This code writes  three sensor readings as  a comma-separated string
# to log.txt on the Pico W flash  memory, then reads the file back and
# splits  the string  into a  list.  Purpose:  Demonstrate basic  file
# writing and  reading in MicroPython  using log.txt to write  to pico
# flash.

# WRITING comma-delimited data to a file

# With real sensorData we would have to convert the values to a string
# and concatinate the strings in a comma seperated list.

# Example temperature readings from three sensors
def run():
    sensorData = "25.5,26.0,24.8"

# You can supply a path to the logfile on the pico, here we just leave
# it in the default directory where our ssd1306.py and main.py are.

# file2picoFlash is the handle/object we use to r/w to log.txt, it can
# be called anything. With the object we can call all the member
# functions on the micropython library for manipulating files. Open
# log.txt in write mode ('w')
    print("We will try to write data to the pico w 2's flash memory")
    with open('log.txt', 'w') as file2picoFlash:
        file2picoFlash.write(sensorData)  # Write the comma-separated string to the file
    print("Data written to log.txt")  # Confirm data was written



# READING comma-delimited data
# with open('log.txt', 'r') as file2picoFlash:  # Open log.txt in read mode ('r')
#     content = file2picoFlash.read()  # Read the entire file as a string
#     print("Raw data:", content)  # Print the raw string
#     # Parse into a list
#     values = content.split(',')  # Split the string at commas to create a list
#     print("Parsed values:", values)  # Print the resulting list
