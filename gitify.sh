#!/bin/bash

# Gitify - add files to a Git repo, one file per commit,
# backdating the commit to the file's modification time.

# The reverse of Rodrigo Silva's "git-restore-mtime" script.

# Silas S. Brown 2019 - public domain - no warranty.

# Might be useful for "git"ifying historical code, as at
# least the file's modification time should put an upper
# limit on when each part was written.

# Top-level dotfiles will NOT be added (so .git itself won't be)

# Use --add to add files to an existing repo,
# or --rewrite to rewrite all.

# --day (optional parameter) limits commits to one per day,
# with the last modification time used in any given day.
# This also ensures all commits are in date order.

unset Day
if test "a$1" == "a--day"; then export Day=1; shift; fi

if test "a$1" == "a--rewrite"; then # (must be run at top-level of the repo)
    mv -i .git/config /tmp/old-git-config || exit 1
    mv -i .git /tmp/old.git
    rm -rf /tmp/old.git &
    git init
    mv /tmp/old-git-config .git/config
elif test "a$1" == "a--add"; then # (this one may also be run in a subdirectory)
    if ! git rev-parse --git-dir >/dev/null 2>/dev/null; then git init; elif git diff | grep . >/dev/null; then git diff; echo "ERROR: Commit these diffs first"; exit 1; fi
else
    echo "Run with --rewrite to delete existing history and rewrite from scratch"
    echo "(in case you've already created a git repo w/out this script)"
    echo "Run with --add to just add new files to the repo"
    echo
    echo "You MUST specify either --rewrite or --add."
    echo "You may also specify --day to limit commits to one per day (and to ensure commits are in date order)."
    exit 1
fi

if test "a$2" == "a--day"; then export Day=1; fi

if test "a$Day" == a1; then
find * -type f -not -name '*~' -not -name .DS_Store -exec python -c 'import os;print(str(os.stat("{}").st_mtime)+" {}")' ';' 2>/dev/null|python -c $'import sys,time,os,pipes\ndef cond(a,b,c):\n if a: return b\n return c\ndf,dt={},{}\nfor d,t,f in sorted([(int(float(l.split()[0])/(24*3600)),float(l.split()[0]),l.split(None,1)[1].rstrip()) for l in sys.stdin]):\n if not d in df: df[d],dt[d]=set(),0\n df[d].add(f);dt[d]=max(dt[d],t)\nfor d in sorted(df.keys()):\n os.environ["GIT_COMMITTER_DATE"]=time.asctime(time.localtime(dt[d]))\n os.system("git add %s && git commit --date=\\"$GIT_COMMITTER_DATE\\" -am \\"add %s\\"" % (" ".join(pipes.quote(x) for x in sorted(df[d])),cond(len(df[d])>5,"%d files" % len(df[d]),", ".join(sorted(df[d])))))'
else
find * -type f -not -name '*~' -not -name .DS_Store -exec git add '{}' ';' -exec bash -c 'export D="$(date -r "{}" 2>/dev/null || stat -f %Sm "{}")";GIT_COMMITTER_DATE="$D" git commit --date="$D" -am "add {}"' ';'
fi && if test "a$1" == "a--rewrite"; then git push -f; fi
