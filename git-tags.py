#!/usr/bin/env python
#  (should work in either Python 2 or Python 3)

# Read versions from the code in old Git commits, and generate version tags
# (TODO: tags for other programs in same repository e.g. annogen in adjuster?)

# If there are multiple commits per version, then the tag for each version is put on the LAST commit in which the code had that version.
# BUT you will need "git push -f --tags" (which may complicate the checkouts of others) if you've made an additional commit without changing a version number that has previously been _pushed_ as a tag.  So for new versions we may have to take "first commit with version number" rather than "last" (see homepage/Makefile and homepage/_doGit2.sh)

# Uncomment one of these:
# version_regex = "v([0-9.]*).*Silas" # jianpu-ly
# version_regex = "Version ([0-9.]*),.*Silas" # midi-beeper, mwr2ly
# version_regex = "Pooler v([0-9.]*)" # PrimerPooler
# version_regex = "Generator.*Version ([0-9.]*)" # css-generator
# version_regex = "lexconvert v([0-9.]*) - convert" # lexconvert
# version_regex = "helper v([0-9.]*).*Silas" # web-typography
# version_regex = "gradint v([0-9.]*).*Silas" # gradint
version_regex = "Adjuster v([0-9.]*).*Silas" # adjuster

try: from subprocess import getoutput # Python 3
except: from commands import getoutput # Python 2
import os, re
version = None
def u(v):
    global version ; version = v
for l in reversed(getoutput(r"git log -p|tr -d $'[\x80-\xff]'").split('\n')):
    # (as we're taking the lines in reverse order, if there are multiple commits per version then the tag for each version should end up on the LAST commit in which the code had that version)
    if l.startswith("+"): re.sub(version_regex,lambda m:u(m.group(1)),l)
    elif l.startswith("commit "):
        commit_id = l.split()[1]
        if version:
            os.system("git tag -d v"+version+" || true")
            os.system("git tag v"+version+" "+commit_id)
os.system("git push --tags")
