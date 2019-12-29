# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import streams  # additional python file holding stream URLs
import subprocess
from gpiozero import LED, Button
import json


def buttonPress():
    player.stop()
    global stationSelected
    stationSelected = incrementStation(stationSelected)
    print("stationSelected =", stationSelected)
    player.set_media(mediaList[stationSelected])
    saveState()
    player.play()


def incrementStation(currentStation):
    if currentStation == (listLength-1): #if last entry
        newStation = 0
    else:
        newStation = currentStation + 1 #increment
    return newStation


def pinARising():                    # Pin A event handler
    if pinB.is_pressed:
        print("CW")   # pin A rising while A is active is a clockwise turn
        global countCW, countCCW
        if countCCW > 0: #reset
            countCW = 0
            countCCW = 0
        else:
            countCW = countCW + 1
        print(countCW, countCCW)


def pinBRising():                    # Pin B event handler
    if pinA.is_pressed:
        print("CCW")    # pin B rising while A is active is a clockwise turn
        global countCW, countCCW
        if countCW > 0:  # reset
            countCW = 0
            countCCW = 0
        else:
            countCCW = countCCW + 1
        print(countCW, countCCW)

def saveState():
    test = 123


#restart pulseaudio, needs to playback audio on most boots
#subprocess.call(["pulseaudio", "-kill"])
#time.sleep(0.5)
#subprocess.call(["pulseaudio", "--start"])
#time.sleep(0.5)

# SETUP
# setup pins
led = LED(pin=27)  # BCM pin
button = Button(pin=17, bounce_time=0.05, hold_time=0.25)  # BCM pin
button.when_pressed = buttonPress
pinA = Button(21, pull_up=True)         # Rotary encoder dt pin connected to BCM pin 21
pinB = Button(20, pull_up=True)         # Rotary encoder clk pin connected to BCM pin 20

countCW = 0
countCCW = 0


# read json file and load data
with open("radioState.json", "r") as f:
    radioState = json.load(f)
stationSelected = radioState["stationSelected"]
# import URLs for streams from streams.py
streamList = streams.streamList
listLength = len(streamList)

# define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
# define VLC player
player = instance.media_player_new()
# define VLC media
mediaList = []
for i in range(listLength):
    mediaList.append(instance.media_new(streamList[i]))

player.audio_set_volume(100)


player.set_media(mediaList[stationSelected])
player.play()

pinA.when_pressed = pinARising      # Register the event handler for pin A
pinB.when_pressed = pinBRising      # Register the event handler for pin B

while True:
    test = 123
