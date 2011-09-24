#!/usr/bin/env python
# TODO:
# - check if target exists and skip of so
# - do I want a hierarchy?
# - put band - album - title in filename
# - do I want lower rez for more songs?
# - lame itself can add --tt title, -ta artist, --tl album 

import sys
from subprocess import Popen, PIPE

STRIP="/usr/local/media/music/"
OUT_DIR="/home/chris/Music/mp3"
LAME_OPTS="--vbr-new -V 2 -B 256 "

for flacpath in sys.argv[1:]:
    flac = flacpath.replace(STRIP, '')
    print "Flac=", flac
    artist, album, title = flac.split('/')
    title = title.replace('.flac', '')
    print "artist='%s' album='%s' title='%s'" % (artist, album, title)
    mp3path = "%s/%s.mp3" % (OUT_DIR, title)
    # file of title only will be clashy
    p1 = Popen(["flac", "-c", "-d", "-s", flacpath], stdout=PIPE)
    lamecmd = ["lame", "--vbr-new", "-V", "2", "-B", "256", "-", mp3path]
    p2 = Popen(lamecmd, stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    id3out = Popen(["id3v2", "-a", artist, "-A", album, "-t", title, mp3path], stdout=PIPE).communicate()[0]
