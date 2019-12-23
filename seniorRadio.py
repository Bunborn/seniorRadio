# Brandon Stevens
# 12/22/2019
#

import vlc
import time
import streams


#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

streamList = streams.streamList
#Define VLC player
player=instance.media_player_new()

mediaList = []

listLength = len(streamList)
#Define VLC media
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

    #soundFile = vlc.MediaPlayer(streamList[i])
    #soundFile.play()
    #time.sleep(10)
    #soundFile.stop()

#Play the media
player.play()
player.audio_set_volume(100)
time.sleep(5)

