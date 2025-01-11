__name__ = "Micro Tracker 32 Emitter"
__author__ = "wwwqr"
__desc__ = "A esp32 project that uses the esp32 now protocol to find his friends"
__version__ = "0.0.1"

import uos
import network
import espnow
import time
from ucryptolib import aes

key = b"bmarfanCkasb6b6c740b1c60K1c5445f"
iv = b"secret-iv-123456"
MODE_CBC = 2
channel = 1
msg = "Im here!"

def encrypt(str):
    cipher = aes(key, MODE_CBC, iv)
    padded = str + " " * (16 - len(str) % 16)
    return cipher.encrypt(padded)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)
peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'
e.add_peer(peer)
realMsg = '{ "protocol": { "name": "micro-tracker-32", "version": "' + __version__ + '" }, "payload": { "channel": ' + str(channel) + ', "msg": "' + msg + '" } }'
    
print("Emitting...")
while True: e.send(peer, encrypt(realMsg), True)