# Wi-Fi Probe Request Scanner
This script scans and logs all the Wi-Fi Probe Requests emitted by any Wi-Fi devices in the neighbourhood.

Data collected :
 - Wi-Fi MAC address
 - Manufacturer of the Wi-Fi adapter
 - SSID of your Wi-Fi access point
 - Signal strength

## Requirements
Several packages are required to be installed in order to execute the Wi-Fi Probe Request Scanner.

Git, Python 3 and aircrack-ng :
```
sudo apt-get install git python3 aircrack-ng
```

Scapy :
```
git clone https://github.com/secdev/scapy.git
cd scapy
sudo python3 setup.py install
```

Netaddr :
```
git clone https://github.com/drkjam/netaddr.git
cd netaddr
sudo python3 setup.py install
```

Finally, it is necessary to turn the Wi-Fi adapter into its monitor mode and to create a folder called `logs`for the future scanned Wi-Fi Probe Requests. Note that you may have to change the name of the Wi-Fi adapter into the script (constant `WIFI_INTERFACE`).
```
sudo airmon-ng start wlan0
mkdir logs
```

## Execution
```
sudo python3 wifi_probe_request_scanner.py
```
