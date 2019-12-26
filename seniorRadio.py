# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import streams  # additional python file holding stream URLs
import subprocess
from gpiozero import LED, Button


def buttonPress():
    global buttonPressCounter
    print("buttonPressCounter =", buttonPressCounter)
    buttonPressCounter = buttonPressCounter + 1

#restart pulseaudio, needs to playback audio on most boots
subprocess.call(["pulseaudio", "-kill"])
time.sleep(0.5)
subprocess.call(["pulseaudio", "--start"])
time.sleep(0.5)

# setup
led = LED(pin=27)  # BCM pin
button = Button(pin=17, bounce_time=0.05)  # BCM pin
buttonPressCounter = 0
button.when_pressed = buttonPress
# define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

# import URLs for streams from streams.py
streamList = streams.streamList
listLength = len(streamList)

# define VLC player
player = instance.media_player_new()

# Define VLC media
mediaList = []
for i in range(listLength):
    mediaList.append(instance.media_new(streamList[i]))

# Set and play player media
for i in range(listLength):
    player.set_media(mediaList[i])
    print(mediaList[i])
    print(i)
    player.play()
    time.sleep(10)
    player.stop()

player.audio_set_volume(100)
