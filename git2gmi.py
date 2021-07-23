#!/usr/bin/env python3

"""git2gmi: summarise commit messages from a user's GitHub repositories as a Gemini markup file
Silas S. Brown 2021, public domain"""

from urllib.request import urlopen
import re, json, sys
try: user = sys.argv[1]
except:
    sys.stderr.write(__doc__+"\nNeed GitHub user name as parameter\n")
    sys.exit(1)
max_earliest_date = None ; commitList = []
for repository in json.loads(urlopen("https://api.github.com/users/"+user+"/repos").read()):
    repository = repository["name"]
    for commit in json.loads(urlopen("https://api.github.com/repos/"+user+"/"+repository+"/commits?per_page=100").read()): # 100 is maximum allowed
        fullDate = commit["commit"]["committer"]["date"]
        date = fullDate[:fullDate.index('T')]
        message = commit["commit"]["message"]
        url = commit["html_url"]
        commitList.append((date,fullDate,"=> %s %s %s: %s" % (url,date,repository,message)))
    if not max_earliest_date: max_earliest_date = date
    elif date: max_earliest_date = max(date,max_earliest_date)
print ("# Recent commits to "+user+"'s GitHub repositories\n"+"\n".join(x[-1] for x in reversed(sorted(commitList)) if x[0] >= max_earliest_date))
