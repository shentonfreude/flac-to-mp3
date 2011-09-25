===========
FLAC to MP3
===========

I've digitized my CDs to lossless FLAC for playing on my Squeezebox
audio devices and have a good sized archive.  But I'd like to listen
to them on my (Android) phone and Nook.  These don't have much storage
so I want to compress them and am willing to trade fidelity for size.

The current archive is organized hierarchically by Artist then Album then Song, like:

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

Work in Progress
================

I hacked it together shortly before going on a road trip so it doesn't
act the way I want, the way described above. Yet.


Requirements
============

The script is in Python and it uses the binaries:

 * `flac`: decode flac files
 * `lame`: encode mp3 file
 * `metaflac`: pulling metadata from flac file like Artist, Album, Title
 * `id3v2`: save metadata to mp3 file

Command Line
============

Presently it is not hierarchichal and gets the list of *files* from
the commandline. Ooutput location is hardcoded.

Metadata
========

It's pretty dumb about finding and extrating metadata.  I'm pretty
dumb myself about extracting metadata and coverart and figuring out
where to pull from FLAC and push into MP3.

