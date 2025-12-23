
from https://ssb22.user.srcf.net/s60/cdrdao.html
(also [mirrored on GitLab Pages](https://ssb22.gitlab.io/s60/cdrdao.html) just in case)

# Spaced-out audio tracks with cdrdao
Sometimes it is desirable to write an audio CD with extra silence between the tracks, so you can play just one selected track and not have to rush to stop the player before the next track starts.  This might be the case for example if the CD contains Gradint practise sessions, or accompaniment music for group singing.

[This Python script](cdrdao.py) (works in both Python 2 and Python 3) takes the tracks as audio files on the command line, converts them with `sox`, and creates `.toc` files for `cdrdao`.  Any extra space on the CD is distributed evenly as silence between the tracks, and if multiple CDs are required then the script will also try to distribute the tracks evenly across CDs (while keeping them in order).  CD-TEXT labels from the original filenames are also added.

## Adding silence to MP3 files
If an MP3 player is in use instead of a CD player, and there is still no “play one track and stop” option, then you’ll either have to add silence to the MP3 files, or add extra silent files “in between” the files.  How to do the latter depends on which ID3 field (if any) the player uses for indexing, so the former is perhaps more straightforward.

Appending silent MP3 frames, including via `mpgedit` or `vbrfix`, doesn’t work with all forms of metadata on all players—Apple products are particularly fussy—so it might be best to re-code the file.  This does mean possible loss of sound quality, and loss of metadata, but you can at least try to ensure the quality is set adequately and the title is copied over.  Something like this (adjust quality setting and length of silence appropriately):

`for N in *.mp3; do (sox "$N" -t raw -r 44100 -c 2 -s -2 -;dd if=/dev/zero bs=84672 count=10000)|lame -V 0 -r -s 44.1 - --tt "$(echo $(mpg123 --long-tag -n 1 "$N" 2>&1 | grep '^[^A-Za-z]*Title'|sed -e 's/^[^A-Za-z]*Title://'))" -o tmp.mp3 ; mv tmp.mp3 "$N"; done`

## Copyright and Trademarks
All material © Silas S. Brown unless otherwise stated.
Apple is a trademark of Apple Inc.
MP3 is a trademark that was registered in Europe to Hypermedia GmbH Webcasting but I was unable to confirm its current holder.
Python is a trademark of the Python Software Foundation.
Any other trademarks I mentioned without realising are trademarks of their respective holders.
