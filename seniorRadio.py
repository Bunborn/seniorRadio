# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import streams #additional python file holding stream URLs
import gpiozero
from gpiozero import LED, Button

#setup
#led = LED(11)
#button = Button(13)
#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#import URLs for streams from streams.py
streamList = streams.streamList
listLength = len(streamList)


led.on()
time.sleep(1)
led.off()
time.sleep(1)
button.when_pressed = led.on
button.when_released = led.off

#define VLC player
player=instance.media_player_new()


#Define VLC media
mediaList = []
for i in range(listLength):
    mediaList.append(instance.media_new(streamList[i]))


#Set and play player media
for i in range(listLength):
    player.set_media(mediaList[i])
    print(mediaList[i])
    print(i)
    player.play()
    time.sleep(10)
    player.stop()

player.audio_set_volume(100)

