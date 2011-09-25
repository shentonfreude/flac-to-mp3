===========
FLAC to MP3
===========

I've digitized my CDs to lossless FLAC for playing on my Squeezebox
audio devices and have a good sized archive.  But I'd like to listen
to them on my (Android) phone and Nook.  These don't have much storage
so I want to compress them and am willing to trade fidelity for size.

The current archive is organized hierarchically by Artist then Album
then Song, like:

  Made Out of Babies
  * Coward
    ...
  * The Ruiner
    - 01 Cooker.flac
    ...
    - 09 How to Get Bigger.flac
    - cover.jpg

I'd like to preserve that hierarchy in the generated MP3s so that it's
easy to navigate on a dumb device's filesystem.

I know, I know: this is well-trodden ground. I didn't find anything
that did quite what I wanted. And as the Rifleman's Creed says: "There
are many like it, but this one is mine."

Usage
=====

Specify source and destination directories and optional bitrate::

  ./flac-to-mp3.py /PATH/TO/FLAC/ARTISTS /PATH/TO/MP3/DIRS BITRATE

For example:

  ./flac-to-mp3.py /usr/local/media/music/ ~/Music/mp3 64

The default bitrate is 64 Kbps, which is a bit low but allows me to
fit more on my old iPod, Android, or Nook.


Requirements
============

The script is in Python and it uses the binaries:

 * `flac`: decode flac files
 * `lame`: encode mp3 file
 * `metaflac`: pulling metadata from flac file like Artist, Album, Title
 * `id3v2`: save metadata to mp3 file

Metadata
========

It tries to pull metadata including artist, album, title, track
number, genre, and date from the FLAC.  If it can't, it tags the MP3
with the artist, album, track name from the FLAC file path and name.
