#!/usr/bin/env python2

# Apache log alerts, Silas S. Brown 2019, public domain.

# In late 2019, various IP addresses in China started downloading
# the complete (3M+) CedPane file 30,000 times (40x/day/IP), probably
# due to somebody writing an application very badly.
# I had to redirect that user-agent on that file to a
# "please be nice to my server" message (which may or may
# not have been read by a human).

# This script is meant to check through Apache log files
# and alert of any similar behaviour earlier.

log_file = "/var/log/apache2/user/ssb22/access.log"

min_bytes_to_report = 5000000 # less than this per IP = IP won't be reported no matter how many requests
min_requests_to_report = 10 # less than this per IP = IP won't be reported no matter how many bytes
min_sameFile_to_report = 2 # must contain at least N attempts on the same file to be reported
max_age = 25*3600 # ignore log lines older than this

import sys,time

ipBytes,ipReqs,ipURLCounts,ipLog = {},{},{},{}
for l in open(log_file):
    ip,_,_,date,tz,get,url,method,code,size,rest = l.split(None,10)
    if time.time()-time.mktime(time.strptime(date[1:],"%d/%b/%Y:%H:%M:%S")) > max_age: continue
    ipBytes[ip]=ipBytes.get(ip,0)+int(size)
    ipReqs[ip]=ipReqs.get(ip,0)+1
    ipURLCounts.setdefault(ip,{})[url]=ipURLCounts.setdefault(ip,{}).get(url,0)+1
    ipLog.setdefault(ip,[]).append(l.strip())
o = []
for ip in ipBytes.keys():
    if ipBytes[ip] < min_bytes_to_report: continue
    if ipReqs[ip] < min_requests_to_report: continue
    if all(v<min_sameFile_to_report for v in ipURLCounts[ip].values()): continue
    o.append("\n".join(ipLog[ip]))
sys.stdout.write("\n\n".join(o)+"\n")
