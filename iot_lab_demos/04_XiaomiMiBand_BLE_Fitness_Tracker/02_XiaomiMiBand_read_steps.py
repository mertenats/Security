#!/usr/bin/python

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging, time

# Xiaomi Mi Band 1S - Read Steps Counter - Demo
# MAC address: 11:22:33:44:55:66

UUID_CHARACTERISTIC_REALTIME_STEPS  = '0000ff06-0000-1000-8000-00805f9b34fb'

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

adapter = pygatt.GATTToolBackend()

def getSteps():
    bytearray = device.char_read(UUID_CHARACTERISTIC_REALTIME_STEPS)
    if bytearray[1] != 0:
        return bytearray[0] + bytearray[1] * 256
    return bytearray[0]

try:
    adapter.start()
    # connect to the device
    device = adapter.connect('11:22:33:44:55:66')
    print('Connected to the device')
    print('Press CTRL+C to stop this program ...\n')

    try:
        while True:
            print 'Actual number of steps: %d' % getSteps()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

finally:
    adapter.stop()
