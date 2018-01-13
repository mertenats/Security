#!/usr/bin/python

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging, time

# Xiaomi Mi Band 1S - Activate Alarm - Demo
# MAC address: 11:22:33:44:55:66

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    # connect to the device
    device = adapter.connect('11:22:33:44:55:66')
    print('Connected to the device')

    # turn on the alarm
    device.char_write('00002a06-0000-1000-8000-00805f9b34fb', bytearray([0x02]))
    print('Alarm activated')

    time.sleep(5)
finally:
    adapter.stop()
