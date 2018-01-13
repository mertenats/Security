#!/usr/bin/python3

# Requirements:
#  - pyshark:   https://pypi.python.org/pypi/pyshark
#  - tshark:    sudo apt-get install tshark

import pyshark

# Noke Device Address
# sudo hcitool lescan
DEVICE_ADDRESS = '11:22:33:44:55:66'
# Wireshark filter and file location
WIRESHARK_CAPTURE_FILTER = 'btle.slave_bd_addr == ' + DEVICE_ADDRESS + ' && (btatt.opcode == 0x1b || btatt.opcode == 0x52)'
WIRESHARK_CAPTURE_PATH = 'Wireshark/Noke_Wireshark_capture.pcapng'
# output file name
OUTPUT_FILE_PATH = 'Tmp/01_Noke_Wireshark_capture_encrypted_values.txt'

# open the capture and filter the BLE packets
wiresharkCapture = pyshark.FileCapture(WIRESHARK_CAPTURE_PATH, display_filter=WIRESHARK_CAPTURE_FILTER)
# create a file to write the dissected values
outputFile = open(OUTPUT_FILE_PATH, 'w')

# loop through the packets and write all BLE ATT values into the file
for packet in wiresharkCapture:
    value = str(packet['BTATT'].value).replace(':', '')[:32]
    outputFile.writelines(value + '\n')
    print(value)

outputFile.close()
