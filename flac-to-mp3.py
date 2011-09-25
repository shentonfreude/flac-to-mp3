#!/usr/bin/env python
# TODO:
# - use flag to skip or overwrite if target exists
# - how to get FLAC metadata from files like 9353 created by Grip?
#   metaflac can't find anything in them but strings does
# - lame itself can add --tt title, -ta artist, --tl album 

import logging
import os
import sys
from subprocess import Popen, PIPE

# The bitrate may not change the size with VBR?

LAME_CMD = ['lame', '--vbr-new', '-V', '2']
LAME_BITRATE = '64'
LAME_BITRATES = (32,40,48,56,64,80,96,112,128,160,192,224,256,320)

if len(sys.argv) not in (3,4):
    raise RuntimeError("Usage: %s FLAC_TOP_DIR MP3_DEST_DIR [BITRATE]" % sys.argv[0])

TOP_DIR=sys.argv[1]             # holds all artists
DEST_DIR=sys.argv[2]
if len(sys.argv) > 3:
    LAME_BITRATE = sys.argv[3]
    if not int(LAME_BITRATE) in LAME_BITRATES:
        raise RuntimeError("LAME bitrate=%s not in list=%s" % (
                LAME_BITRATE, LAME_BITRATES))
LAME_CMD += ['-B', LAME_BITRATE]
logging.warning("Setting bitrate to %s" % LAME_BITRATE)

def get_flac_tag(tag, flac_path):
    TAGS = ('ARTIST', 'TITLE', 'ALBUM', 'GENRE', 'TRACKNUMBER', 'DATE')
    if not tag in TAGS:
        raise RuntimeError("Tag=%s not valid, use: %s" % (tag, TAGS))
    metaflac = Popen(["metaflac", "--show-tag=%s" % tag, flac_path],
                 stdout=PIPE).communicate()[0]
    if metaflac:
        metaflac = metaflac.split('=')[1].strip()
    return metaflac

for artist in sorted(os.listdir(TOP_DIR)):
    artist_path = os.path.join(TOP_DIR, artist)
    if not os.path.isdir(artist_path):
        logging.warning("Skipping, not an artist dirctory: %s" % artist_path)
        continue
    for album in sorted(os.listdir(artist_path)):
        album_path = os.path.join(TOP_DIR, artist, album)
        if not os.path.isdir(album_path):
            logging.warning("Skipping, not an album dirctory: %s" % album_path)
            continue
        for flac in sorted(os.listdir(album_path)):
            flac_path = os.path.join(TOP_DIR, artist, album, flac)
            if not os.path.isfile(flac_path):
                logging.warning("Skipping, flac is not a file: %s" % flac_path)
                continue
            if not flac.endswith('.flac'):
                logging.warning("Skipping, not an .flac file: %s" % flac_path)
                continue
            print "file artist=%s  album=%s flac=%s" % (artist, album, flac)

            flac_artist = get_flac_tag('ARTIST',      flac_path)
            flac_album  = get_flac_tag('ALBUM',       flac_path)
            flac_title  = get_flac_tag('TITLE',       flac_path)
            flac_track  = get_flac_tag('TRACKNUMBER', flac_path)
            flac_genre  = get_flac_tag('GENRE',       flac_path)
            flac_date   = get_flac_tag('DATE',        flac_path)
            print "flac artist=%s  album=%s title=%s track=%s genre=%s date=%s" % (
                flac_artist, flac_album, flac_title,
                flac_track, flac_genre, flac_date)

            title = flac_title or flac.replace('.flac', '')
            mp3_artist = flac_artist or artist
            mp3_album  = flac_album  or album
            mp3_title  = flac_title  or title
            print "mp3  artist=%s  album=%s title=%s" % (
                mp3_artist, mp3_album, mp3_title)


            dest_dir = os.path.join(DEST_DIR, artist, album)
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)
            dest_path = os.path.join(dest_dir, "%s.mp3" % title)
            # test for existence and skip?
            if os.path.isfile(dest_path):
                logging.warning("NOT overwriting extant destination file=%s" % dest_path)
                continue
            lame_cmd = LAME_CMD + ['-', dest_path]
            p1 = Popen(["flac", "-c", "-d", "-s", flac_path], stdout=PIPE)
            p2 = Popen(lame_cmd, stdin=p1.stdout, stdout=PIPE)
            p1.stdout.close()
            output = p2.communicate()[0]
            id3out = Popen(["id3v2",
                            "--artist", mp3_artist,
                            "--album",  mp3_album,
                            "--song",   mp3_title,
                            "--track",  flac_track,
                            "--genre",  flac_genre,
                            "--year",   flac_date,
                            dest_path], stdout=PIPE).communicate()[0]

