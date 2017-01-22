#!/usr/local/bin/python
import sys

from soco import SoCo

sonos_ip = "YOUR_IP_HERE"
help_msg = "Usage: commandutil.py [cmd]\nValid commands:\n\
help \t-- show this help message\n\
info \t-- show info about the Sonos speaker\n\
play [url | track_no] \t-- play the current item\n\
\ta URL of a file may be specified or one of the pre-loaded tracks\n\
tracks \t-- show pre-loaded tracks\n\
pause \t-- pause the currently playing track\n\
stop \t-- stop the currently playing track\n\
next \t-- go to the next track\n\
prev \t-- go back to the previous track\n\
current -- show info about the currently playing song\n\
volume \t-- set the volume level (0 - 100)\n\
mute [true | false] \t-- show mute status or set to true or false\n"

song_urls = [
    "https://archive.org/download/MozartK626Requiem3.DiesIrae/MozartK626Requiem3.DiesIrae.mp3",
    "http://mp3fb.com/static/ixFWzb7aWiiHlVHRla8Uq4ihxNe2RZCTNznJnUiixHI/Sir%2Bmix%2Ba%2Blot%2B-%2BI%2Blike%2Bbig%2Bbutts.mp3",
    "http://soundbible.com/mp3/Screaming%20Female-SoundBible.com-414994458.mp3",
    "http://soundbible.com/mp3/Evil%20Yelling-SoundBible.com-1774362373.mp3",
    "http://soundbible.com/mp3/Werewolf%20Howl-SoundBible.com-1888553688.mp3"
]
songs = [
    'Requiem - Dies Irae by Mozart',
    'I Like Big Butts by Sir Mix A-Lot',
    'Screaming Woman',
    'Evil Yelling',
    'Werewolf Howl'
]

if __name__ == '__main__':

    sonos = SoCo(sonos_ip)
    cmd = 'help' if len(sys.argv) < 2 else sys.argv[1].lower()
    
    if cmd == 'help':
        print help_msg
    elif cmd == 'info':
        all_info = sonos.get_speaker_info()
        for item in all_info:
            print "%s: %s" % (item, all_info[item])
        print "volume: " + str(sonos.volume()) + "/100"
        print "muted: %s" % ("false" if sonos.mute() == 0 else "true")
    elif cmd == 'play':
        if len(sys.argv) == 2:
            print sonos.play()
        elif len(sys.argv) == 3:
            try:
                track_no = int(sys.argv[2])
                print sonos.play_uri(uri=song_urls[track_no - 1])
            except ValueError:
                print sonos.play_uri(uri=sys.argv[2])
    elif cmd == 'tracks':
        print "Tracks:"
        index = 0
        for song in songs:
            print str(index + 1) + ": " + songs[index]
            index = index + 1
        print ""
    elif cmd == 'pause':
        print sonos.pause()
    elif cmd == 'stop':
        print sonos.stop()
    elif cmd == 'next':
        print sonos.next()
    elif cmd == 'prev':
        print sonos.previous()
    elif cmd == 'current':
        track = sonos.get_current_track_info()
        print 'Current track: ' + track['artist'] + ' - ' + track['title'] + \
        '\nFrom album ' + track['album'] + \
        '\nTrack number ' + track['playlist_position'] + ' in the playlist' + \
        '\nDuration: ' + track['duration'] + ' minutes' + \
        '\nVolume: ' + str(sonos.volume()) + '/100'
    elif cmd == 'volume':
        if len(sys.argv) == 3:
            try:
                print sonos.volume(int(sys.argv[2]))
            except ValueError:
                print "Must enter an integer from 0 - 100"
        else:
            print "Must specify a volume level (0 - 100)"
    elif cmd == 'mute':
        if len(sys.argv) == 3:
            if sys.argv[2] == "true":
                print sonos.mute(1)
            elif sys.argv[2] == "false":
                print sonos.mute(0)
            else:
                print "Must specify 'true' or 'false' for muting"
        else:
            print "Sonos is currently %s" % ("unmuted" if sonos.mute() == 0 else "muted")
    else:
        print help_msg
