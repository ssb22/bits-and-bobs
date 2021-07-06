#!/bin/bash
# 
# Set up push access to GitHub, GitLab, GitLab-cam, Bitbucket, Gitee
# (for repositories already created / imported across these platforms)
# 
# Syntax: repo-setup [--shallow] all | repo names
# (all = all public repositories;
# any NOT in the list is assumed not to have mirrors)
# 
All="CedPane PrimerPooler adjuster css-generator web-imap-etc config lexconvert indexer web-typography jianpu-ly mwr2ly midi-beeper scan-reflow bits-and-bobs router-scripts wm6-utils s60-utils gradint yali-voice yali-lower cameron-voice 4dml old-web-access-gateway clara-empricost"
IsIn() { N="$1"; shift; for i in $*; do if [ "$i" == "$N" ] ; then return 0; fi; done; false ; }
if [ "$1" == "" ]; then
    echo "Syntax: repo-setup [--shallow] all | repo names"
    exit 1
elif [ "$1" == --shallow ]; then
    export RepoSetupShallowClone="--depth=1"
    shift
elif ! [ "$RepoSetupShallowClone" == "--depth=1" ]; then
    unset RepoSetupShallowClone
fi
if [ "$1" == all ]; then
    exec "$0" $All
fi
while ! [ "$1" == "" ]; do
  export N=$(echo "$1"|tr -d /) # in case of auto-complete
  if ! [ -e "$N" ]; then git clone $RepoSetupShallowClone git@github.com:ssb22/$N.git || exit 1; fi
  if ! [ -d "$N" ]; then shift; continue; fi # so you can run with * in a dir with files as well
  # Otherwise put the settings in on an already-cloned repo:
  cd $N || exit 1
  if IsIn $N $All; then
  git remote set-url origin --push --delete . 2>/dev/null >/dev/null || true
  git remote set-url origin --push git@github.com:ssb22/$N.git || exit 1
  git remote set-url origin --push --add git@gitlab.com:ssb22/$N.git || exit 1
  git remote set-url origin --push --add git@gitlab.developers.cam.ac.uk:ssb22/$N.git || exit 1 # (beta service provided to cam.ac.uk members)
  git remote set-url origin --push --add git@bitbucket.org:ssb22/$(echo $N|tr A-Z a-z).git || exit 1
  git remote set-url origin --push --add git@gitee.com:ssb22/$(echo $N|sed -e s/^4/four/).git || exit 1
  else echo "Not adding mirrors to $N (not in All)"
  fi
  git config user.name "Silas S. Brown"
  git config user.email ssb22@cam.ac.uk
  cd ..
  echo "Set up $N"
  shift
done
