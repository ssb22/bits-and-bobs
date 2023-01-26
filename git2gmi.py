#!/usr/bin/env python3

"""git2gmi: summarise commit messages from a user's GitHub repositories as a Gemini markup file
Silas S. Brown 2021-23, public domain"""

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

from urllib.request import urlopen
import re, json, sys
try: user = sys.argv[1]
except:
    sys.stderr.write(__doc__+"\nNeed GitHub user name as parameter\n")
    sys.exit(1)
max_earliest_date = None ; commitList = []
for repository in json.loads(urlopen("https://api.github.com/users/"+user+"/repos").read()):
    is_fork = repository["fork"]
    repository = repository["name"]
    count = 0
    for commit in json.loads(urlopen("https://api.github.com/repos/"+user+"/"+repository+"/commits?per_page=100").read()): # 100 is maximum allowed
        count += 1
        if is_fork and not user in commit["commit"]["author"]["email"]: continue # don't log other people's commits on our forks (assumes Git username is part of our email)
        fullDate = commit["commit"]["committer"]["date"]
        date = fullDate[:fullDate.index('T')]
        message = commit["commit"]["message"]
        url = commit["html_url"]
        if message.startswith("Merge") and "\n\n" in message: message=message[:message.index("\n\n")] # because commits themselves will be listed separately
        else: message = message.replace("\n\n","\n",1) # probably "This reverts commit N", don't need blank line before
        commitList.append((date,fullDate,"=> %s %s %s: %s" % (url,date,repository,message)))
    if count>=100 and not is_fork:
        if not max_earliest_date: max_earliest_date = date
        elif date: max_earliest_date = max(date,max_earliest_date)
print ("# Recent commits to "+user+"'s GitHub repositories\n"+"\n".join(x[-1] for x in reversed(sorted(commitList)) if not max_earliest_date or x[0] >= max_earliest_date))
