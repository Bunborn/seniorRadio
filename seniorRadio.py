# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import subprocess
from gpiozero import LED, Button #for rpi IO
import json


def buttonPress():
    print("button press yo")


def changeStation():
    player.stop()
    player.set_media(mediaList[stationSelected])
    saveState()
    player.play()


def incrementStation(currentStation):
    if currentStation == (len(streamURLs) - 1):  # if last entry
        newStation = 0
    else:
        newStation = currentStation + 1  # increment
    return newStation


def decrementStation(currentStation):
    if currentStation == 0:  # if first entry
        newStation = (len(streamURLs) - 1)
    else:
        newStation = currentStation - 1  # decrement
    return newStation

def increaseAudio(audioLevel):
    if audioLevel == 100:  # if max
        newAudio = 100
    else:
        newAudio = audioLevel + 10  # increase
    return newAudio


def decreaseAudio(audioLevel):
    if audioLevel == 0:  # if min
        newAudio = 0
    else:
        newAudio = audioLevel - 10  # decrease
    return newAudio


def pinARising():  # Pin A station event handler
    if pinB.is_pressed:
        print("Station CW")  # pin A rising while A is active is a clockwise turn
        global stationDialCountCW, stationDialCountCCW
        if stationDialCountCCW > 0:  # reset, debouncer
            stationDialCountCW = 0
            stationDialCountCCW = 0
        else:
            stationDialCountCW = stationDialCountCW + 1
        print(stationDialCountCW, stationDialCountCCW)


def pinBRising():  # Pin B station event handler
    if pinA.is_pressed:
        print("Station CCW")  # pin B rising while A is active is a counter-clockwise turn
        global stationDialCountCW, stationDialCountCCW
        if stationDialCountCW > 0:  # reset, debouncer
            stationDialCountCW = 0
            stationDialCountCCW = 0
        else:
            stationDialCountCCW = stationDialCountCCW + 1
        print(stationDialCountCW, stationDialCountCCW)


def pinCRising():  # Pin C audio level event handler
    if pinD.is_pressed:
        print("Audio CW")  # pin C rising while C is active is a clockwise turn
        global audioDialCountCW, audioDialCountCCW
        if audioDialCountCCW > 0:  # reset, debouncer
            audioDialCountCW = 0
            audioDialCountCCW = 0
        else:
            audioDialCountCW = audioDialCountCW + 1
        print(audioDialCountCW, audioDialCountCCW)

def pinDRising():  # Pin D audio level event handler
    if pinC.is_pressed:
        print("Audio CCW")  # pin D rising while C is active is a counter-clockwise turn
        global audioDialCountCW, audioDialCountCCW
        if audioDialCountCW > 0:  # reset, debouncer
            audioDialCountCW = 0
            audioDialCountCCW = 0
        else:
            audioDialCountCW = audioDialCountCW + 1
        print(audioDialCountCW, audioDialCountCCW)


def saveState():
    radioState["stationSelected"] = stationSelected
    radioState["audioLevel"] = 100
    with open("radioState.json", "w") as f:
        json.dump(radioState, f, indent=4)


# restart pulseaudio, needs to playback audio on most boots
# subprocess.call(["pulseaudio", "-kill"])
# time.sleep(0.5)
# subprocess.call(["pulseaudio", "--start"])
# time.sleep(0.5)

# SETUP
# setup pins
led = LED(pin=27)  # BCM pin
led.on()
button = Button(pin=17, bounce_time=0.05, hold_time=0.25)  # BCM pin
button.when_pressed = buttonPress
pinA = Button(21, pull_up=True)  # Station rotary encoder dt pin connected to BCM pin 21
pinB = Button(20, pull_up=True)  # Station rotary encoder clk pin connected to BCM pin 20
pinC = Button(19, pull_up=True)  # Audio level rotary encoder dt pin connected to BCM pin
pinD = Button(16, pull_up=True)  # Audio level rotary encoder clk pin connected to BCM pin

#  global variables
stationDialCountCW = 0
stationDialCountCCW = 0
audioDialCountCW = 0
audioDialCountCCW = 0

# read json file and load data
with open("radioState.json", "r") as f:
    radioState = json.load(f)
stationSelected = radioState["stationSelected"]
audioLevel = radioState["audioLevel"]
streamURLs = radioState["stationLinks"]
streamNames = radioState["stationNames"]

# setup VLC
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
mediaList = [] #list for each stream
for i in range(len(streamURLs)):
    mediaList.append(instance.media_new(streamURLs[i]))

player.audio_set_volume(audioLevel)
player.set_media(mediaList[stationSelected])

player.play()

pinA.when_pressed = pinARising  # Register the station event handler for pin A
pinB.when_pressed = pinBRising  # Register the station event handler for pin B
pinC.when_pressed = pinCRising  # Register the audio level event handler for pin C
pinD.when_pressed = pinDRising  # Register the audio level event handler for pin D

while True:
    # main loop, poll to see dials change with debouncing
    if stationDialCountCW >= 5:  # valid turn
        stationSelected = incrementStation(stationSelected)
        changeStation()
        stationDialCountCW = 0
    elif stationDialCountCCW >= 5:  # valid turn
        stationSelected = decrementStation(stationSelected)
        changeStation()
        stationDialCountCCW = 0
    if audioDialCountCW >= 3:  # likely valid turn
        audioLevel = increaseAudio(audioLevel)
        print("audio level:", audioLevel)
        player.audio_set_volume(audioLevel)
        saveState()
        audioDialCountCW = 0
    elif audioDialCountCCW >= 3:  # likely valid turn
        audioLevel = decreaseAudio(audioLevel)
        print("audio level:", audioLevel)
        player.audio_set_volume(audioLevel)
        saveState()
        audioDialCountCCW = 0
