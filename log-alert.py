#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# Apache log alerts, Silas S. Brown 2019/21/23-24, public domain, no warranty.

# In late 2019, various IP addresses in China started downloading
# the complete (~3M) CedPane file 30,000 times (40x/day/IP),
# probably due to somebody writing an application very badly.
# (Some of the requests stopped short of the full file, so my guess is
# it's a search application and the full downloads were failed queries.)
# Furthermore, this client would not negotiate gzip with the HTTP server
# so it was doing full uncompressed traffic every time.
# I eventually changed the download into a zip file
# (and divided up the HTML version) to discourage this.

# This script is meant to check through Apache log files
# and alert of any similar behaviour earlier.

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

log_file = "/var/log/apache2/user/ssb22/access.log"

min_bytes_to_report = 7000000 # less than this per IP = IP won't be reported no matter how many requests
min_requests_to_report = 10 # less than this per IP = IP won't be reported no matter how many bytes
min_sameFile_to_report = 7 # must contain at least N attempts on the same file to be reported
min_sameFile_size = 1000000 # and in total across all attempts (ignore browsers failing to cache small css files)
max_age = 25*3600 # ignore log lines older than this

import sys,time
try: from commands import getoutput # Python 2
except ImportError: from subprocess import getoutput # Python 3

ipBytes,ipReqs,ipURLCounts,ipURLSizes,ipLog = {},{},{},{},{}
for l in open(log_file):
    ip,_,_,date,tz,get,url,method,code,size,rest = l.split(None,10)
    if time.time()-time.mktime(time.strptime(date[1:],"%d/%b/%Y:%H:%M:%S")) > max_age: continue
    ipBytes[ip]=ipBytes.get(ip,0)+int(size)
    ipReqs[ip]=ipReqs.get(ip,0)+1
    if not ipURLCounts.setdefault(ip,{}).setdefault(url,0) or not code=="206":
        ipURLCounts[ip][url] += 1
        ipURLSizes.setdefault(ip,{}).setdefault(url,[]).append(int(size))
    ipLog.setdefault(ip,[]).append(l.strip())
o = []
for ip in ipBytes.keys():
    if ipBytes[ip] < min_bytes_to_report: continue
    if ipReqs[ip] < min_requests_to_report: continue
    concern = [url for url,counts in ipURLCounts[ip].items() if counts>=min_sameFile_to_report and sum(ipURLSizes[ip][url]) >= min_sameFile_size]
    if concern: o.append("\n".join(["%s fetched %d bytes in %d reqs" % (ip,ipBytes[ip],len(ipLog[ip]))]+[getoutput("whois '"+ip.replace("'","")+"'|egrep -i '^(orgname|descr):'").strip()]+["URLs of concern:"]+concern+["log entries:"]+ipLog[ip]))
if o: sys.stdout.write("\n\n".join(["Potential cause for concern: %d IP(s)" % len(o)]+o)+"\n")
