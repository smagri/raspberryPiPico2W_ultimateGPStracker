# This code writes three sensor readings as a comma-separated string to log.txt
# on the Pico W, then reads the file back and splits the string into a list.
# Purpose: Demonstrate basic file writing and reading in MicroPython using log.txt.

# Writing comma-delimited data to a file
sensorData = "25.5,26.0,24.8"  # Example temperature readings from three sensors

with open('log.txt', 'w') as file:  # Open log.txt in write mode ('w')
    file.write(sensorData)  # Write the comma-separated string to the file
print("Data written to log.txt")  # Confirm data was written

# Reading comma-delimited data
# with open('log.txt', 'r') as file:  # Open log.txt in read mode ('r')
#     content = file.read()  # Read the entire file as a string
#     print("Raw data:", content)  # Print the raw string
#     # Parse into a list
#     values = content.split(',')  # Split the string at commas to create a list
#     print("Parsed values:", values)  # Print the resulting list
