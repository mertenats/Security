#!/usr/bin/python

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging, time

# Magic Blue - Change colors - Demo
# MAC address: 11:22:33:44:55:66

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    # connect to the device
    device = adapter.connect('11:22:33:44:55:66')
    print('Connected to the device')

    # turn on the bulb
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0xcc, 0x23, 0x33]))
    print('Bulb turned ON')

    time.sleep(3)

    # turn it red
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0x56, 0xff, 0x00, 0x00, 0x00, 0xf0, 0xaa]))
    print('Bulb set to RED')

    time.sleep(3)

    # turn it green
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0x56, 0x00, 0xff, 0x00, 0x00, 0xf0, 0xaa]))
    print('Bulb set to GREEN')

    time.sleep(3)

    # turn it blue
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0x56, 0x00, 0x00, 0x0ff, 0x00, 0xf0, 0xaa]))
    print('Bulb set to BLUE')

    time.sleep(3)

    # turn it white
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0x56, 0xff, 0xff, 0xff, 0x00, 0xf0, 0xaa]))
    print('Bulb set to WHITE')

    time.sleep(3)

    # turn off the bulb
    device.char_write('0000ffe9-0000-1000-8000-00805f9b34fb', bytearray([0xcc, 0x24, 0x33]))
    print('Bulb turned OFF')
finally:
    adapter.stop()
