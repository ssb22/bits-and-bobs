#!/bin/bash

# Script to make Safari 6's "Reader" mode narrower for use with
# magnification, and to change Reader mode's colours.

# Silas S. Brown 2012,2019,2021-22 - public domain - no warranty

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

if [ ! "$FgCol" ]; then
  echo -n "HTML foreground colour (default black): "
  read FgCol
  if [ ! "$FgCol" ]; then FgCol=black; fi
fi
if [ ! "$BgCol" ]; then
  echo -n "HTML background colour (default grey): "
  read BgCol
  if [ ! "$BgCol" ]; then BgCol=grey; fi
  # (might be easier on the eyes than white if you don't
  # want to invert the colours.  Inverting the colours might
  # require a different selection of fonts for readability.)
fi

if [ ! "$1" ]; then
  # Try to find Reader.html
  Found=0
  RH=/Applications/Safari.app/Contents/Resources/Reader.html # Safari 5.0
  if [ -e "$RH" ]; then "$0" "$RH" || exit 1; Found=1; fi
  RH=/System/Library/PrivateFrameworks/Safari.framework/Resources/Reader.html # Safari 5.1
  if [ -e "$RH" ]; then "$0" "$RH" || exit 1; Found=1; fi
  RH=/System/Library/StagedFrameworks/Safari/Safari.framework/Versions/A/Resources/Reader.html # Safari 6.0
  if [ -e "$RH" ]; then "$0" "$RH" || exit 1; Found=1; fi

  if [ $Found = 0 ]; then
    echo "Error: cannot find Safari's Reader.html"
    if locate Reader.html|grep Safari; then
      echo "It might be one of the above (update the script?)"
    fi
    echo "Aborting."
    exit 1
  else exit 0; fi
fi

if ! [ -e "$1" ]; then
  echo "Error: reader template at $1 does not exist"
  exit 1
fi

RHOrig="$1.orig"
if [ -e "$RHOrig" ] && ! diff "$1" "$RHOrig" >/dev/null; then
  echo "$RHOrig already exists"
  echo "and differs from $1"
  echo "Aborting to avoid possible problems."
  exit 1
fi

if ! sudo cp "$1" "$RHOrig"; then exit 1; fi

if sed -e 's/width: 6\([0-9][0-9]px\)/width: 3\1/g' -e 's/width: 8\([0-9][0-9]px\)/width: 5\1/g' -e "s/white;/WaSwHiTe;/g" -e "s/black/$FgCol/g" -e "s/WaSwHiTe/$BgCol/g" < "$RHOrig" | grep -v 'left:' | sudo bash -c "cat > '$1'"; then echo "Changes made"; fi
