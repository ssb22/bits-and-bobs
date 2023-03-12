#!/bin/bash

# Gitify - add files to a Git repo, one file per commit,
# backdating the commit to the file's modification time.

# The reverse of Rodrigo Silva's "git-restore-mtime" script.

# v1.55, Silas S. Brown 2019-23, public domain, no warranty

# Might be useful for "git"ifying historical code, as at
# least the file's modification time should put an upper
# limit on when each part was written.

# Top-level dotfiles will NOT be added (so .git itself won't be).
# Changed files will be "added" as changes (unless using --rewrite).

# Use --add to add to an existing repository,
# or --rewrite to rewrite all.

# If an existing repository's commits didn't
# capture the correct timestamps, use --restamp
# (restamps existing files, does not add new ones,
# you can use --add on a separate run afterwards)

# Use --addpush to behave like --add but do a "git push"
# after every commit (might be useful on connections that
# cannot do a large push at the end).  This can be used
# only if you've already done "git init" and any necessary
# "git remote add origin" commands.

# --day (optional parameter) limits commits to one per day,
# with the last modification time used in any given day.
# This also ensures all commits are in date order.

# Where to find history of this script:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

unset Day
if [ "$1" = "--day" ]; then Day=1; shift; fi
if [ "$2" = "--day" ]; then Day=1; fi
if which python 2>/dev/null >/dev/null; then Python=python; elif which python3 2>/dev/null >/dev/null; then Python=python3; elif which python2.7 2>/dev/null >/dev/null; then Python=python2.7; else echo "Cannot find python (now required)"; exit 1; fi

if [ "$1" = "--rewrite" ]; then # (must be run at top-level of the repo)
    mv -i .git/config /tmp/old-git-config || exit 1
    mv -i .git /tmp/old.git
    rm -rf /tmp/old.git &
    git init
    mv /tmp/old-git-config .git/config
elif [ "$1" = "--add" ] || [ "$1" = "--restamp" ]; then # (these may be run at top level or in a subdirectory of the repo)
    if ! git rev-parse --git-dir >/dev/null 2>/dev/null; then git init; fi
elif [ "$1" = "--addpush" ]; then # (this one may also be run either at top level or in a subdir)
    if ! git rev-parse --git-dir >/dev/null 2>/dev/null; then echo "ERROR: --addpush requires an already-existing repository"; exit 1; fi # otherwise how will we know where to push it?
else
    echo "Run with --rewrite to delete existing history and rewrite from scratch"
    echo "(in case you've already created a git repo w/out this script)"
    echo "Run with --add to just add new files to the repo"
    echo "(or --addpush to do this while pushing every commit)"
    echo "Run with --restamp correct timestamps of files in repo (without adding more)"
    echo
    echo "You MUST specify one of the above switches."
    echo "You may also specify --day to limit commits to one per day (and to ensure commits are in date order)."
    exit 1
fi

FilesList="$(mktemp)"
if [ "$1" = "--restamp" ]; then
    git rm -rf --cached . | sed -e 's/^rm .//' -e 's/.$//' > "$FilesList"
    git commit -am "removal + timestamp correction"
else
    find -- * -type f -not -name '*~' -not -name .DS_Store > "$FilesList" 2>/dev/null
fi
Branch="$(git branch | grep '^\*' | sed -e 's/..//')"
if [ "$Day" = 1 ]; then
  if [ "$1" = "--addpush" ]; then export ExtraCmd="git push -u origin $Branch"; else unset ExtraCmd; fi
  $Python -c $'import sys,time,os,pipes\ndef cond(a,b,c):\n if a: return b\n return c\ndf,dt={},{}\nfor d,t,f in sorted([(int(l[0]/(24*3600)),l[0],l[1].rstrip()) for l in [(os.stat(a[:-1]).st_mtime,a[:-1]) for a in sys.stdin if os.path.exists(a[:-1])]]):\n if not d in df: df[d],dt[d]=set(),0\n df[d].add(f);dt[d]=max(dt[d],t)\nfor d in sorted(df.keys()):\n os.environ["GIT_COMMITTER_DATE"]=time.asctime(time.localtime(dt[d]))\n for x in sorted(df[d]): os.system("git add -v "+pipes.quote(x))\n r=os.system("git commit --date=\\"$GIT_COMMITTER_DATE\\" -am \\"add %s\\"" % (cond(len(df[d])>5,"%d files" % len(df[d]),", ".join(sorted(df[d]))),))\n if "ExtraCmd" in os.environ and not r and os.system(os.environ["ExtraCmd"]): raise Exception("git push failed or interrupted")' < "$FilesList"
  # (if files already added, 'git commit' will fail and 'git push' won't happen; if one 'git push' fails, next one will be larger, so we check for fail so interrupt / resume is easier)
else
  if [ "$1" = "--addpush" ]; then Extras=" ; git push -u origin $Branch"; else unset Extras; fi
  $Python -c 'import sys;sys.stdout.write(sys.stdin.read().replace("\n","\0"))' < "$FilesList"|xargs -0 -L 1 bash -c 'git add "$0"||exit 1;D="$(date -r "$0" 2>/dev/null || stat -f %Sm "$0")";GIT_COMMITTER_DATE="$D" git commit --date="$D" -am "add $0"'"$Extras"
fi && if [ "$1" = "--rewrite" ]; then git push -f; fi; rm "$FilesList"; exit
