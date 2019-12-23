# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import streams


#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#import URLs for streams from streams.py
streamList = streams.streamList
listLength = len(streamList)

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
    time.sleep(5)
    player.stop()

player.audio_set_volume(100)

