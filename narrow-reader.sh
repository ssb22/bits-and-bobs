#!/bin/bash

# Script to make Safari's "Reader" mode narrower for use with Zoom
# and to change Reader mode's colours.

# Silas S. Brown 2012,2019 - public domain - no warranty

if [ ! "$FgCol" ]; then
  echo -n "HTML foreground colour (default black): "
  read FgCol
  if [ ! "$FgCol" ]; then export FgCol=black; fi
fi
if [ ! "$BgCol" ]; then
  echo -n "HTML background colour (default grey): "
  read BgCol
  if [! "$BgCol" ]; then export BgCol=grey; fi
  # (might be easier on the eyes than white if you don't
  # want to invert the colours.  Inverting the colours might
  # require a different selection of fonts for readability.)
fi

if [ ! "$1" ]; then
  # Try to find Reader.html
  export Found=0

  export RH=/Applications/Safari.app/Contents/Resources/Reader.html # Safari 5.0
  if test -e "$RH"; then "$0" "$RH" || exit 1; export Found=1; fi
  export RH=/System/Library/PrivateFrameworks/Safari.framework/Resources/Reader.html # Safari 5.1
  if test -e "$RH"; then "$0" "$RH" || exit 1; export Found=1; fi
  export RH=/System/Library/StagedFrameworks/Safari/Safari.framework/Versions/A/Resources/Reader.html # Safari 6.0
  if test -e "$RH"; then "$0" "$RH" || exit 1; export Found=1; fi

  if test $Found == 0; then
    echo "Error: cannot find Safari's Reader.html"
    if locate Reader.html|grep Safari; then
      echo "It might be one of the above (update the script?)"
    fi
    echo "Aborting."
    exit 1
  else exit 0; fi
fi

if ! test -e "$1"; then
  echo "Error: reader template at $1 does not exist"
  exit 1
fi

export RHOrig="$(echo $1).orig"
if test -e "$RHOrig" && ! diff "$1" "$RHOrig" >/dev/null; then
  echo "$RHOrig already exists"
  echo "and differs from $1"
  echo "Aborting to avoid possible problems."
  exit 1
fi

if ! sudo cp "$1" "$RHOrig"; then exit 1; fi

if sed -e 's/width: 6\([0-9][0-9]px\)/width: 3\1/g' -e 's/width: 8\([0-9][0-9]px\)/width: 5\1/g' -e "s/white;/WaSwHiTe;/g" -e "s/black/$FgCol/g" -e "s/WaSwHiTe/$BgCol/g" < "$RHOrig" | grep -v 'left:' | sudo bash -c "cat > '$1'"; then echo "Changes made"; fi
