#!/usr/bin/env python

# Script to keep a command running on the DS machines
# (which can't run processes unless user is logged in),
# and/or to keep an SSH tunnel open to them
# (as .authorized_keys not readable unless logged in)
# Silas S. Brown, public domain, no warranty

import pty,os,sys,signal,time

hosts = ["ds1","ds2"] # to be tried round-robin, in case one gets stuck
p = open(os.environ["HOME"]+"/.ssh/ds").read().strip()
command = ' '.join(sys.argv[1:])
if not command: command = 'python2 imapfix.py'
cmd_keepalive = int(os.environ.get("cmd_keepalive","2000")) # works for imapfix if imapfix_config has quiet=False: IMAP IDLE timeout is lower than this
# If just a tunnel, could use "while true; do sleep 999;date;done"
ip_file = os.environ.get("ip_file","") # e.g. ".ip" , to write our IP address when we connect (in place of Dynamic DNS); quote it if necessary

os.chdir("/dev/shm")
def log(s):
  if type("")==type(u"") and not type(s)==type(""): s=s.decode('latin1') # Python 3
  try: s=(open("log-ds").read()+s)[-65536:]
  except: pass
  open("log-ds","w").write(s)
if type("")==type(u""): p,command,ip_file=p.encode('latin1'),command.encode('latin1'),ip_file.encode('latin1')
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
    ss = b""
    while b'assword:' not in ss:
        ss = os.read(master,1024)
        log(ss)
        if b'sure' in ss: os.write(master,b'yes\r')
        if time.time()>t+30: raise Exception("Took too long")
        time.sleep(3)
    os.write(master,p+b'\r')
    time.sleep(5)
    log(os.read(master,1024)) ; time.sleep(5)
    if not os.path.exists('dspath'): raise Exception("dspath was removed")
    if ip_file: os.write(master,b" echo $SSH_CLIENT|cut -d' ' -f1 > "+ip_file+b";")
    os.write(master,b' '+command+b'; exit\r')
    last_activity = time.time()
    while True:
        r=os.read(master,1024)
        if r:
          if time.time()>last_activity+300: log(" [time=%02d:%02d] " % time.localtime()[3:5])
          log(r)
          last_activity = time.time()
        elif time.time() > last_activity + cmd_keepalive: raise Exception("Application quiet for too long: stuck?")
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
