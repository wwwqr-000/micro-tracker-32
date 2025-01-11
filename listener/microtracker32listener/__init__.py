__name__ = "Micro Tracker 32 Listener"
__author__ = "wwwqr"
__desc__ = "A esp32 project that uses the esp32 now protocol to find his friends"
__version__ = "0.0.1"

import uos
import network
import espnow
from machine import Pin
from time import sleep
from ucryptolib import aes
import json

key = b"bmarfanCkasb6b6c740b1c60K1c5445a"
iv = b"secret-iv-123458"
MODE_CBC = 2
channel = 1

def decrypt(str):
    cipher = aes(key, MODE_CBC, iv)
    return cipher.decrypt(str)

sta = network.WLAN(network.STA_IF)
sta.active(True)
e = espnow.ESPNow()
e.active(True)

while True:
    sleep(0.01)
    host, msg = e.recv()
    if (not msg): continue
    try: msg = decrypt(msg)
    except Exception: continue
    msg = msg.strip()
    try: packet = json.loads(msg)
    except Exception: continue
    if (packet['protocol']['name'] != "micro-tracker-32" or packet['protocol']['version'] != __version__): continue
    print(packet)
