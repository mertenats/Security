# Bluetooth Low Energy Advertising Scanner
This script scans and logs all the Advertising packets emitted by any Bluetooth LE devices in the neighbourhood.

Data collected :
  - Timestamp
  - BLE Address
  - Manufacturer (optional)
  - BLE Address Type
  - Signal Strength (RSSI)
  - BLE Device Connectable
  - Device Name (optional)

## Requirements
Several packages are required to be installed in order to execute the Bluetooth LE Advertising Scanner.

Git and Python 3 ::
```
sudo apt-get install git python3 python3-pip
```

Netaddr :
```
git clone https://github.com/drkjam/netaddr.git
cd netaddr
sudo python3 setup.py install
```

Bluepy :
```
sudo apt-get install libglib2.0-dev
sudo pip3 install bluepy
```

Finally, it is necessary to create a folder called `logs`for the future scanned BLE Advertising packets. Note that you may have to change the name of the Bluetooth adapter into the script (constant `BLE_INTERFACE`).
```
mkdir logs
```

## Execution
```
sudo python3 ble_advertising_scanner.py
```
