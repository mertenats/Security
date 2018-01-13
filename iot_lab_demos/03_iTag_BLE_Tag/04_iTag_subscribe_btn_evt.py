#!/usr/bin/python

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging

# iTag Tag - Subscribe to button events - Demo
# MAC address: 11:22:33:44:55:66

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

adapter = pygatt.GATTToolBackend()

def onButtonPressedCallback(handle, value):
    print('Button pressed')

try:
    adapter.start()
    # connect to the device
    device = adapter.connect('11:22:33:44:55:66')
    print('Connected to the device')

    # subscribe to the button state characteristic
    device.subscribe('0000ffe1-0000-1000-8000-00805f9b34fb', callback=onButtonPressedCallback)

    raw_input('Press any key to stop this program ...\n')
finally:
    adapter.stop()
