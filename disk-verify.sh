#!/bin/bash

# Hard disk verify script
# Silas S. Brown, public domain, no warranty

# If you can't run a filing system with its own checking
# (ZFS or Btrfs,
# or fusecompress with incompressible removed from source)
# and you're not sure the device's CRC/ECC/etc is enough,
# then you could do this to check files haven't changed if
# their timestamps etc are still the same.

# Note: on a moderately-sized hard disk (500 GB), this can
# take hours to run and generate anything 0.5-1 GB files.

# You will likely get one or two benign changes where some
# program really has updated its data file but keeping the
# same timestamp and size.
# e.g. Chromium caches, OpenCL maps

# Sometimes only the "-" line of an md5sum is shown, due
# to it being followed in the diff by the "-" lines of
# subsequently-listed changed-files before the "+" line;
# this is normal.

if ! [ -e /.md5sums ]; then
  echo "Building initial /.md5sums"
  find -sx /[^.dpt]* -type f -ls -exec md5sum '{}' ';' > /.md5sums
else
  find -sx /[^.dpt]* -type f -ls -exec md5sum '{}' ';' > /.md5sums2
  if ! diff -u /.md5sums /.md5sums2 | awk 'BEGIN { sameDate=0 } /^ [^ ]+ +[0-9]/ { sameDate=1 } /^[+-][0-9a-fA-F]+ +\// { if (sameDate) print } /^[^ ]+ +[0-9]/ { sameDate=0 }' | grep .; then
    mv -v /.md5sums2 /.md5sums
  else mv -i /.md5sums2 /.md5sums; fi
fi
