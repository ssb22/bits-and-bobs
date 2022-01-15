#!/usr/bin/env python2
import commands,pty,os,sys,signal,time
os.chdir("/dev/shm")
hosts = ["ds1","ds2"] # to be tried round-robin, in case one gets stuck
p = open(os.environ["HOME"]+"/.ssh/ds").read().strip()
def log(s):
  try: s=(open("log-ds").read()+s)[-65536:]
  except: pass
  open("log-ds","w").write(s)
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
        log(ss)
        if 'sure' in ss: os.write(master,'yes\r')
        if time.time()>t+30: raise Exception("Took too long")
        time.sleep(3)
    os.write(master,p+'\r')
    time.sleep(5)
    log(os.read(master,1024)) ; time.sleep(5)
    if not os.path.exists('dspath'): raise Exception("Not exists")
    os.write(master,' python2 imapfix.py; exit\r')
    last_activity = time.time()
    while True:
        r=os.read(master,1024) ; log(r)
        if r: last_activity = time.time()
        elif time.time() > last_activity + 2000: raise Exception("No activity for some time longer than IMAP IDLE timeout: stuck?") # assumes imapfix_config quiet=False
        time.sleep(5)
        if not os.path.exists('dspath'): raise Exception("Not exists from loop")
  except SystemExit: raise
  except:
      log("\nException: "+str(sys.exc_info()[1])+"\n")
      try: os.kill(pid,signal.SIGTERM)
      except: pass
      time.sleep(1)
      try: os.kill(pid,signal.SIGKILL)
      except: pass
      os.wait() # don't want defunct process cluttering pi's table
      time.sleep(60) # and retry
