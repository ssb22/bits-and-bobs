#!/bin/bash
wget -N http://people.ds.cam.ac.uk/ssb22/setup/ssh-android.sh http://people.ds.cam.ac.uk/ssb22/mwrhome/offline-updater.py http://people.ds.cam.ac.uk/ssb22/notes/flatplan.py http://people.ds.cam.ac.uk/ssb22/notes/notesorg_lua.txt http://people.ds.cam.ac.uk/ssb22/notes/notesorg_macro.txt http://people.ds.cam.ac.uk/ssb22/papers/notesorg.py http://people.ds.cam.ac.uk/ssb22/s60/cdrdao.py http://people.ds.cam.ac.uk/ssb22/setup/riscos-time.py http://people.ds.cam.ac.uk/ssb22/setup/pounce.py http://people.ds.cam.ac.uk/ssb22/setup/record-skype.py http://people.ds.cam.ac.uk/ssb22/setup/msn-rename.py http://people.ds.cam.ac.uk/ssb22/setup/narrow-reader.sh http://people.ds.cam.ac.uk/ssb22/setup/macvoices.txt http://people.ds.cam.ac.uk/ssb22/setup/openid-cli.py
git commit -am "Update $(echo $(git diff|grep '^--- a/'|sed -e 's,^--- a/,,')|sed -e 's/ /, /g')" && git push
