#!/bin/bash
# 
# Set up push access to GitHub, GitLab and BitBucket
# so git-sync.sh scripts will work from ssb22's account.
# (Assumes the repositories have already been created / imported.)
# 
if test "a$1" == a; then echo "Missing repo name"; exit 1; fi
while ! test "a$1" == a; do
  export N=$(echo "$1"|tr -d /) # in case of auto-complete
  if ! test -e "$N"; then git clone git@github.com:ssb22/$N.git || exit 1; fi
  if ! test -d "$N"; then shift; continue; fi # so you can run with * in a dir with files as well
  # Otherwise put the settings in on an already-cloned repo:
  cd $N || exit 1
  git remote set-url origin --push --delete . 2>/dev/null >/dev/null || true
  git remote set-url origin --push git@github.com:ssb22/$N.git || exit 1
  git remote set-url origin --push --add git@gitlab.com:ssb22/$N.git || exit 1
  git remote set-url origin --push --add git@gitlab.developers.cam.ac.uk:ssb22/$N.git || exit 1 # (beta service provided to cam.ac.uk members)
  git remote set-url origin --push --add git@bitbucket.org:ssb22/$(echo $N|tr A-Z a-z).git || exit 1
  git config user.name "Silas S. Brown"
  git config user.email ssb22@cam.ac.uk
  cd ..
  echo "Set up $N"
  shift
done
