#!/usr/bin/env python3

"""git2gmi: summarise commit messages from a user's GitHub repositories as a Gemini markup file
Silas S. Brown 2021-25, public domain, no warranty"""

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

# Example output: gemini://gemini.ctrl-c.club/~ssb22/git.gmi
# and gemini://tilde.pink/~ssb22/git.gmi

from dateutil import parser # pip install python-dateutil
from urllib.request import urlopen
import re, json, sys, time
try: user = sys.argv[1]
except:
    sys.stderr.write(__doc__+"\nNeed GitHub user name as parameter\n")
    sys.exit(1)
max_earliest_date = None ; commitList = []
for repository in json.loads(urlopen("https://api.github.com/users/"+user+"/repos?per_page=100").read()):
    is_fork = repository["fork"]
    repository = repository["name"]
    count = 0
    for commit in json.loads(urlopen("https://api.github.com/repos/"+user+"/"+repository+"/commits?per_page=100").read()): # 100 is maximum allowed
        count += 1
        if not user in commit["commit"]["author"]["email"]: continue # (assumes Git username is part of our email) don't log other people's commits here (if it's a fork, we don't want to log others' commits before we forked, and if it's not a fork, for any pull request we'll see the merge commit, so don't also need to log the history of the branch here)
        fullDate = commit["commit"]["committer"]["date"]
        date = "%d-%02d-%02d" % time.localtime(parser.parse(fullDate).timestamp())[:3] # parse and re-construct, because UTC vs BST in near-midnight commits can affect the reported date
        message = commit["commit"]["message"]
        url = commit["html_url"]
        if message.startswith("Merge") and "\n\n" in message: message=message[:message.index("\n\n")] # because commits themselves will be listed separately
        else: message = message.replace("\n\n","\n",1) # probably "This reverts commit N", don't need blank line before
        i=message.find("\nThis reverts commit ")
        if i>0: message=message[:i]
        commitList.append((date,fullDate,"=> %s %s %s: %s" % (url.replace("https://github.com","https://www.github.com",1),date,repository,message))) # .replace() to work around a bug in deedum 2022.0406 for Android: if GitHub's own app is also installed on the same device, deedum says "Cannot find app to handle https://github.com", but with www is OK
    if count>=100 and not is_fork:
        if not max_earliest_date: max_earliest_date = date
        elif date: max_earliest_date = max(date,max_earliest_date)
print ("# Recent commits to "+user+"'s GitHub repositories\n"+"\n".join(x[-1] for x in reversed(sorted(commitList)) if not max_earliest_date or x[0] >= max_earliest_date))
