#!/usr/bin/env python2
import commands,pty,os,signal,time,signal
os.chdir("/dev/shm")
hosts = ["ds1","ds2"] # to be tried round-robin, in case one gets stuck
p = open("/home/ssb22/.ssh/ds").read().strip()
hPtr = 0
while True:
  try:
    pid, master = pty.fork()
    if not pid: # child
        os.execvp('/usr/bin/ssh', ['ssh', '-o', 'ControlMaster=yes', '-o', 'ControlPath=dspath', '-o', 'Compression=yes', '-o', 'ConnectionAttempts=9', '-o', 'ServerAliveInterval=60', hosts[hPtr]])
        raise SystemExit
    hPtr += 1
    if hPtr==len(hosts): hPtr = 0
    t=time.time()
    ss = ""
    while 'assword:' not in ss:
        ss = os.read(master,1024)
        if 'sure' in ss: os.write(master,'yes\r')
        if time.time()>t+30: raise Exception("Took too long")
        time.sleep(3)
    os.write(master,p+'\r')
    time.sleep(5) ; os.read(master,1024) ; time.sleep(5)
    if not os.path.exists('dspath'): raise Exception("Not exists")
    os.write(master,' python2 imapfix.py; exit\r')
    while True:
        r=os.read(master,1024) ; time.sleep(5)
        if not os.path.exists('dspath'): raise Exception("Not exists from loop, last read="+repr(r)+", this read="+repr(os.read(master,1024)))
  except SystemExit: raise
  except:
      try: os.kill(pid,signal.SIGTERM)
      except: pass
      time.sleep(1)
      try: os.kill(pid,signal.SIGKILL)
      except: pass
      os.wait() # don't want defunct process cluttering pi's table
      time.sleep(60) # and retry
