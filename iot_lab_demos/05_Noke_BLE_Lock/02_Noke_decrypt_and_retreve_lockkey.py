#!/usr/bin/python3

import sys
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

# input file name
INPUT_FILE_PATH = 'Tmp/01_Noke_Wireshark_capture_encrypted_values.txt'
# output file name
OUTPUT_FILE_PATH = 'Tmp/02_Noke_Wireshark_capture_decrypted_values.txt'
OUTPUT_FILE_PATH_LOCK_key = 'Tmp/03_Noke_Wireshark_capture_lock_key.txt'

types = {
    1: 'SESSION_START              ',
    2: 'SESSION_START_CONFIGURATION',
    6: 'UNLOCK_REQUEST             ',
    7: 'UNLOCK_RESPONSE            ',
    8: 'BATTERY_REQUEST            ',
    9: 'BATTERY_RESPONSE           '
}

def main():
    outputFile = open(OUTPUT_FILE_PATH, 'w')
    aesKey = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    cipher = AES.new(aesKey, AES.MODE_ECB)

    with open(INPUT_FILE_PATH) as inputFile:
        for value in inputFile:
            # remove \n
            ciphertext = value[:32]
            # convert the value in bytes
            ciphertext = bytes(unhexlify(ciphertext))
            # decrypt the value
            message = cipher.decrypt(ciphertext)

            if message[0] != 0x7e:
                # try again with the initial key
                cipher = AES.new(aesKey, AES.MODE_ECB)
                message = cipher.decrypt(ciphertext)

                if message[0] != 0x7e:
                    print(hexlify(ciphertext).decode() + ' -> CIPHERTEXT NOT DECRYPTABLE')
                    outputFile.write(hexlify(ciphertext).decode() + ' -> CIPHERTEXT NOT DECRYPTABLE\n')
                    continue

            # get message type and length
            length = message[1]
            type = message[2]

            if type == 2:
                # generate a new AES key
                nonce1 = b'\x00\x00\x00\x00'
                nonce2 = message[3: message[1] - 1]
                xornonce = bytes([a ^ b for a, b in zip(nonce1, nonce2)])
                newAesKey = bytes(aesKey[0:5]) + bytes([(a + b) % 256 for a, b in zip(aesKey[5:9], xornonce)]) + bytes(aesKey[9:16])
                cipher = AES.new(newAesKey, AES.MODE_ECB)

            if type == 6:
                print(hexlify(ciphertext).decode() + ' -> ' + hexlify(message).decode() + ' -> ' + types[type] + '\tData: ' + hexlify(message[3: length - 1]).decode() + '  <- LOCK KEY')
                outputFile.write(hexlify(ciphertext).decode() + ' -> ' + hexlify(message).decode() + ' -> ' + types[type] + '\tData: ' + hexlify(message[3: length - 1]).decode() + '  <- LOCK KEY\n')
                outputFileLockKey = open(OUTPUT_FILE_PATH_LOCK_key, 'w')
                outputFileLockKey.write(hexlify(message[3: length - 1]).decode())
                outputFileLockKey.close()
            else:
                print(hexlify(ciphertext).decode() + ' -> ' + hexlify(message).decode() + ' -> ' + types[type] + '\tData: ' + hexlify(message[3: length - 1]).decode())
                outputFile.write(hexlify(ciphertext).decode() + ' -> ' + hexlify(message).decode() + ' -> ' + types[type] + '\tData: ' + hexlify(message[3: length - 1]).decode() + '\n')

    inputFile.close()
    outputFile.close()


if __name__ == "__main__":
    main()