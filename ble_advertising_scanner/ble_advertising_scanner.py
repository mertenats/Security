#!/usr/bin/env python3

"""

    BLE Advertising Scanner

    Logs :
        - Timestamp
        - BLE Address
        - Manufacturer (optional)
        - BLE Address Type
        - Signal Strength (RSSI)
        - BLE Device Connectable
        - Device Name (optional)

    Requirements :
        - bluepy:   https://github.com/IanHarvey/bluepy
        - netaddr:  https://github.com/drkjam/netaddr

"""

from bluepy.btle import Scanner, DefaultDelegate
import netaddr
import logging
from datetime import datetime

BLE_INTERFACE = 0 # hci0

EXCLUDED_BLE_ADDRESS = [
    '11:22:33:44:55:66'
]

EXCLUDE_BLE_RANDOM_ADDRESS = False

LOGS_DELIMITER = ';'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, device, is_new_device, is_new_data):
        if device.addrType == 'random' and EXCLUDE_BLE_RANDOM_ADDRESS:
            return

        if device.addr not in EXCLUDED_BLE_ADDRESS:
            data = []
            # stores the current time
            data.append(datetime.now().isoformat())
            # stores the BLE Address
            data.append(device.addr)
            # retrieves and stores the manufacturer
            try:
                manufacturer = netaddr.EUI(device.addr)
                data.append(manufacturer.oui.registration().org)
            except netaddr.NotRegisteredError:
                data.append('')
            # stores the BLE Address Type
            data.append(device.addrType)
            # stores the Signal Strength
            data.append(str(device.rssi))
            # stores if the device is connectable or not
            data.append(str(device.connectable))
            # stores the BLE device name
            if not device.getValueText(9) == None:
                data.append(device.getValueText(9))
            else:
                data.append('')
            logging.info(LOGS_DELIMITER.join(data))

def main():
    logging.basicConfig(
        filename = 'logs/'+ __file__ + '.log',
        level = logging.INFO,
        format = '%(message)s'
    )

    scanner = Scanner(BLE_INTERFACE).withDelegate(ScanDelegate())
    try:
        while True:
            scanner.start()
            scanner.process(timeout=5)
            scanner.stop()
            scanner.clear()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()