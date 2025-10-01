# nextbuses.mobi fetch next 2 buses for specific stop
# Silas S. Brown 2025 - public domain - no warranty

busStopCode = "TODO: SET THIS"
import requests, re, time
def untracked(m):
    # assume clock time means untracked
    mins = int((time.mktime(time.localtime()[:3]+tuple(int(x) for x in m.group().split(':'))+time.localtime()[5:])-time.time())/60)
    return "untracked "+str(mins)+" minute"+("" if mins==1 else "s")
print(" and ".join(re.sub("^[0-9]+:[0-9][0-9]",untracked,re.sub(".* (in|at) ","",t.replace("DUE","due").replace("min","minute"))) for t in re.findall('(?<=<p class="Stops">)[^<]*(?=</p>)',requests.get("https://nextbuses.mobi/WebView/BusStopSearch/BusStopSearchResults/"+busStopCode.lower()).content.decode('utf-8'))[:2]))
