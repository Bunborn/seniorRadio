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
    player.play()

def incrementStation(currentStation):
    if currentStation == (listLength-1): #if last entry
        newStation = 0
    else:
        newStation = currentStation + 1 #increment
    return newStation



#restart pulseaudio, needs to playback audio on most boots
#subprocess.call(["pulseaudio", "-kill"])
#time.sleep(0.5)
#subprocess.call(["pulseaudio", "--start"])
#time.sleep(0.5)

# SETUP
# setup gpio
led = LED(pin=27)  # BCM pin
button = Button(pin=17, bounce_time=0.05)  # BCM pin
button.when_pressed = buttonPress
stationSelected = 0

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
# read json file
with open("radioState.json", "r") as jsonContent:
    print(json.load(jsonContent))
player.audio_set_volume(100)

eventChange = 0
player.set_media(mediaList[stationSelected])
player.play()
while True:
    test = 123
