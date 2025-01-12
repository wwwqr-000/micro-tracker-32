__name__ = "Micro Tracker 32 Listener"
__author__ = "wwwqr"
__desc__ = "A esp32 project that uses the esp32 now protocol to find his friends"
__version__ = "0.0.1"

import network
import espnow
import json
import screen
from machine import Pin
from time import sleep
from ucryptolib import aes


key = b"bmarfanCkasb6b6c740b1c60K1c5445f"
iv = b"secret-iv-123456"
MODE_CBC = 2
channel = 1
beepPin = 13
decreaseBtnPin = 12
increaseBtnPin = 14
confirmBtnPin = 27
screenSCL = 26
screenSDA = 25

beep = Pin(beepPin, Pin.OUT)
decreaseBtn = Pin(decreaseBtnPin, Pin.IN, Pin.PULL_UP)
increaseBtn = Pin(increaseBtnPin, Pin.IN, Pin.PULL_UP)
confirmBtn = Pin(confirmBtnPin, Pin.IN, Pin.PULL_UP)
decreaseBtnCooldown = False
increaseBtnCooldown = False
confirmBtnCooldown = False
isInSelectChannelMenu = True

def decrypt(str):
    cipher = aes(key, MODE_CBC, iv)
    return cipher.decrypt(str)

def quickBeep(delay):
    beep.on()
    sleep(0.02)
    beep.off()
    sleep(delay)

sta = network.WLAN(network.STA_IF)
sta.active(True)
e = espnow.ESPNow()
e.active(True)

screen.drawTxt("test", 0, 0)
screen.refresh()

while True:
    sleep(0.01)
    #Button handling
    if (confirmBtn.value() == 0):
        if (not confirmBtnCooldown):
            isInSelectChannelMenu = not isInSelectChannelMenu
        
        confirmBtnCooldown = True
        
    else: confirmBtnCooldown = False
    
    if (decreaseBtn.value() == 0 and isInSelectChannelMenu):
        if (not decreaseBtnCooldown and (channel - 1) >= 1): channel -= 1
        decreaseBtnCooldown = True
        
    else: decreaseBtnCooldown = False
    
    if (increaseBtn.value() == 1 and isInSelectChannelMenu):
        if (not increaseBtnCooldown and (channel + 1) <= 100): channel += 1
        increaseBtnCooldown = True
        
    else: increaseBtnCooldown = False
        
    if (isInSelectChannelMenu):
        screen.cls()
        screen.drawTxt("Select a channel", 0, 0)
        screen.drawTxt("Channel: " + str(channel), 0, 10)
        screen.refresh()
        continue
    
    screen.cls()
    screen.drawTxt("Listening...", 0, 0)
    screen.drawTxt("Channel: " + str(channel), 0, 10)
    
    host, msg = e.recv()
    if (not msg): continue
    try: msg = decrypt(msg)
    except Exception: continue
    msg = msg.strip()
    try: packet = json.loads(msg)
    except Exception: continue
    if (packet['protocol']['name'] != "micro-tracker-32" or packet['protocol']['version'] != __version__ or packet['payload']['channel'] != channel): continue
    screen.drawTxt("(Msg line under)", 0, 20)
    screen.drawTxt(str(packet['payload']['msg']), 0, 30)
    strength = list(e.peers_table.values())[0][0]
    strength += (-strength * 2)
    screen.drawTxt("Signal: " + str(strength), 0, 50)
    quickBeep(strength / 1000)
    screen.refresh()


