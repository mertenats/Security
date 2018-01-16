#!/usr/bin/env python3

"""

    Wi-Fi Probe Request Scanner

    Logs :
        - Timestamp
        - MAC Address
        - Manufacturer (optional)
        - SSID (optional)
        - Signal Strength

    Requirements :
        - scapy:    https://github.com/secdev/scapy
        - netaddr:  https://github.com/drkjam/netaddr

"""

from scapy.all import *
import netaddr
import logging
import base64
from datetime import datetime

WIFI_INTERFACE = 'wlan0mon'
WIFI_PROBE_REQUEST_FILTER = 'type mgt subtype probe-req'

EXCLUDED_WIFI_MAC_ADDRESS = [
    '11:22:33:44:55:66',
    '11:22:33:44:55:66',
    '11:22:33:44:55:66'
]

LOGS_DELIMITER = ';'

def on_wifi_probe_request_calllback(packet):
    try:
        wifi_mac_address = packet.addr2
    except AttributeError:
        return

    try:
        ssid = packet.info.decode()
    except UnicodeDecodeError:
        ssid =  base64.b64encode(packet.info)

    if wifi_mac_address not in EXCLUDED_WIFI_MAC_ADDRESS:
        data = []
        # stores the current time
        data.append(datetime.now().isoformat())
        # stores the Wi-Fi MAC Address
        data.append(wifi_mac_address)
        # retrieves and stores the manufacturer
        try:
            manufacturer = netaddr.EUI(wifi_mac_address)
            data.append(manufacturer.oui.registration().org)
        except netaddr.NotRegisteredError:
            data.append('')
        # stores the SSID
        data.append(ssid)
        # computes and stores the Signal Strength
        #signal_strength = -(256-ord(packet.notdecoded[-4:-3]))
        signal_strength = -(256-ord(packet.notdecoded[-2:-1]))
        data.append(str(signal_strength))
        logging.info(LOGS_DELIMITER.join(data))

def main():
    logging.basicConfig(
        filename = 'logs/'+ __file__ + '.log',
        level = logging.INFO,
        format = '%(message)s'
    )

    sniff(
        iface = WIFI_INTERFACE,
        filter = WIFI_PROBE_REQUEST_FILTER,
        prn = on_wifi_probe_request_calllback
    )

if __name__ == '__main__':
    main()
