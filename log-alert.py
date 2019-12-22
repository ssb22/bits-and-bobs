#!/usr/bin/env python2

# Apache log alerts, Silas S. Brown 2019, public domain.

# In late 2019, various IP addresses in China started downloading
# the complete (~3M) CedPane file 30,000 times (40x/day/IP), probably
# due to somebody writing an application very badly.
# (Some of the requests stopped short of the full file, so my guess is
# it's a search application and the full downloads were failed queries.
# To anyone who writes these: PLEASE STORE THE FILE LOCALLY.)
# I had to redirect their "Chrome/51" user-agent on that file to a
# "please be nice to my server" message (which may or may
# not have been read by a human, but I'm hoping the developer will
# eventually take a look).

# This script is meant to check through Apache log files
# and alert of any similar behaviour earlier.

log_file = "/var/log/apache2/user/ssb22/access.log"

min_bytes_to_report = 5000000 # less than this per IP = IP won't be reported no matter how many requests
min_requests_to_report = 10 # less than this per IP = IP won't be reported no matter how many bytes
min_sameFile_to_report = 7 # must contain at least N attempts on the same file to be reported
min_sameFile_size = 1000000 # and in total across all attempts (ignore browsers failing to cache small css files)
max_age = 25*3600 # ignore log lines older than this

import sys,time

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
    if all(v<min_sameFile_to_report for v in ipURLCounts[ip].values()): continue
    if all((sum(v)<min_sameFile_size or ipURLCounts[ip][k]<min_sameFile_to_report) for k,v in ipURLSizes[ip].items()): continue
    o.append("\n".join(ipLog[ip]))
if o: sys.stdout.write("\n\n".join(o)+"\n")
