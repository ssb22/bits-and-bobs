#!/bin/bash

# Gitify - add files to a Git repo, one file per commit,
# backdating the commit to the file's modification time.

# The reverse of Rodrigo Silva's "git-restore-mtime" script.

# v1.51, Silas S. Brown 2019-22, public domain, no warranty

# Might be useful for "git"ifying historical code, as at
# least the file's modification time should put an upper
# limit on when each part was written.

# Top-level dotfiles will NOT be added (so .git itself won't be).
# Changed files will be "added" as changes (unless using --rewrite).

# Use --add to add to an existing repository,
# or --rewrite to rewrite all.

# Use --addpush to behave like --add but do a "git push"
# after every commit (might be useful on connections that
# cannot do a large push at the end).  This can be used
# only if you've already done "git init" and any necessary
# "git remote add origin" commands.

# --day (optional parameter) limits commits to one per day,
# with the last modification time used in any given day.
# This also ensures all commits are in date order.

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: git clone https://gitee.com/ssb22/bits-and-bobs

unset Day
if [ "$1" = "--day" ]; then Day=1; shift; fi

if [ "$1" = "--rewrite" ]; then # (must be run at top-level of the repo)
    mv -i .git/config /tmp/old-git-config || exit 1
    mv -i .git /tmp/old.git
    rm -rf /tmp/old.git &
    git init
    mv /tmp/old-git-config .git/config
elif [ "$1" = "--add" ]; then # (this one may also be run in a subdirectory)
    if ! git rev-parse --git-dir >/dev/null 2>/dev/null; then git init; fi
elif [ "$1" = "--addpush" ]; then # (this one may also be run in a subdirectory)
    if ! git rev-parse --git-dir >/dev/null 2>/dev/null; then echo "ERROR: --addpush requires an already-existing repository"; exit 1; fi
else
    echo "Run with --rewrite to delete existing history and rewrite from scratch"
    echo "(in case you've already created a git repo w/out this script)"
    echo "Run with --add to just add new files to the repo"
    echo "(or --addpush to do this while pushing every commit)"
    echo
    echo "You MUST specify either --rewrite or --add or --addpush."
    echo "You may also specify --day to limit commits to one per day (and to ensure commits are in date order)."
    exit 1
fi

if [ "$2" = "--day" ]; then Day=1; fi

Branch="$(git branch | grep '^\*' | sed -e 's/..//')"
if [ "$Day" = 1 ]; then
  if [ "$1" = "--addpush" ]; then export ExtraCmd="git push -u origin $Branch"; else unset ExtraCmd; fi
  find -- * -type f -not -name '*~' -not -name .DS_Store -exec python -c 'import os,sys;a=sys.argv[1];print(str(os.stat(a).st_mtime)+" "+a)' '{}' ';' 2>/dev/null|python -c $'import sys,time,os,pipes\ndef cond(a,b,c):\n if a: return b\n return c\ndf,dt={},{}\nfor d,t,f in sorted([(int(float(l.split()[0])/(24*3600)),float(l.split()[0]),l.split(None,1)[1].rstrip()) for l in sys.stdin]):\n if not d in df: df[d],dt[d]=set(),0\n df[d].add(f);dt[d]=max(dt[d],t)\nfor d in sorted(df.keys()):\n os.environ["GIT_COMMITTER_DATE"]=time.asctime(time.localtime(dt[d]))\n for x in sorted(df[d]): os.system("git add -v "+pipes.quote(x))\n r=os.system("git commit --date=\\"$GIT_COMMITTER_DATE\\" -am \\"add %s\\"" % (cond(len(df[d])>5,"%d files" % len(df[d]),", ".join(sorted(df[d]))),))\n if "ExtraCmd" in os.environ and not r and os.system(os.environ["ExtraCmd"]): raise Exception("git push failed or interrupted")'
  # (if files already added, 'git commit' will fail and 'git push' won't happen; if one 'git push' fails, next one will be larger, so we check for fail so interrupt / resume is easier)
else
  if [ "$1" = "--addpush" ]; then Extras="-exec git push -u origin $Branch ;"; else unset Extras; fi
  find -- * -type f -not -name '*~' -not -name .DS_Store -exec bash -c 'git add "$1"||exit 1;D="$(date -r "$1" 2>/dev/null || stat -f %Sm "$1")";GIT_COMMITTER_DATE="$D" git commit --date="$D" -am "add $1"' . '{}' ';' $Extras
fi && if [ "$1" = "--rewrite" ]; then git push -f; fi; exit
