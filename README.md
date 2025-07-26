19jul2025


Raspberry Pi Pico 2 W with RP2350, is the correct firmware file from:
https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
mp_firmware_unofficial_latest.uf2

To flash firmware,  hold down bootsel button while  plugging in power,
then  copy  .uf2 to  RP2350  mass  storage  device that  appears.   If
correctly flassed the mass storage drive will dissapear.

ls /dev/ttyACM0  should now  appear, so  select it  in thonny  and you
should get the miropython prompt.

Test with:
print("hello").