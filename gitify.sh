#!/bin/bash

# Gitify - add files to a Git repo, one file per commit,
# backdating the commit to the file's modification time.

# The reverse of Rodrigo Silva's "git-restore-mtime" script.

# Might be useful for "git"ifying historical code, as at
# least the file's modification time should put an upper
# limit on when each part was written.

# Top-level dotfiles will NOT be added (so .git itself won't be)

# Silas S. Brown 2019 - public domain - no warranty.

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
    exit 1
fi

find * -type f -exec git add '{}' ';' -exec bash -c 'export D="$(date -r "{}" 2>/dev/null || stat -f %Sm "{}")";GIT_COMMITTER_DATE="$D" git commit --date="$D" -am "add {}"' ';' && if test "a$1" == "a--rewrite"; then git push -f; fi
