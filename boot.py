from machine import SPI, Pin
import os, sdcard

def mount_sd():
    try:
        # Create mount point if missing
        try:
            os.mkdir("/sd")
        except OSError:
            pass
    try:
        spi = SPI(1, sck=Pin(14), mosi=Pin(15), miso=Pin(12))
        cs = Pin(13, Pin.OUT)
        sd = sdcard.SDCard(spi, cs)

        # Try mount, ignore if already mounted
        try:
            os.mount(sd, "/sd")
            print("SD mounted at /sd")
        except OSError as e:
            print("SD already mounted or mount error:", e)

    except Exception as e:
        print("SD init failed:", e)
        
mount_sd()
