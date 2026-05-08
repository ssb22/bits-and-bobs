#!/usr/bin/env python
# (should work in either Python 2 or Python 3)

# Where to find history:
# on GitHub at https://github.com/ssb22/bits-and-bobs
# and on GitLab at https://gitlab.com/ssb22/bits-and-bobs
# and on BitBucket https://bitbucket.org/ssb22/bits-and-bobs
# and at https://gitlab.developers.cam.ac.uk/ssb22/bits-and-bobs
# and in China: https://gitee.com/ssb22/bits-and-bobs

print ("OpenID Command-line Authoriser v1.4, Silas S. Brown 2017, 2020, 2025")
print ("(public domain, no warranty)\n")

import sys
try: import openid
except ImportError: sys.stderr.write("Library not found\nTry: sudo apt-get install python"+("3" if type(u"")==type("") else "")+"-openid\n"),sys.exit(1)
try: from openid_config import local_addr, public_endpoint_url, profile
except: sys.stderr.write("openid_config.py not found, please make one\n"),sys.exit(1)
print ("Make sure your home page <head> section has:")
print ('<link rel="openid.server" href="'+public_endpoint_url+'" />\n')
sys.stdout.write("Loading... ") ; sys.stdout.flush()
try: from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler # Python 2
except: from http.server import HTTPServer, BaseHTTPRequestHandler # Python 3
try: from urlparse import urlparse # Python 2
except: from urllib.parse import urlparse # Python 3
try: from cgi import parse_qsl
except: from urllib.parse import parse_qsl
from openid.server import server
from openid.store.memstore import MemoryStore
from openid.extensions import sreg
OpenID = server.Server(MemoryStore(), public_endpoint_url)
try: raw_input
except: raw_input = input # Python 3
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = {}
        for k, v in parse_qsl(urlparse(self.path)[4]):
            query[k] = v
        self.handleQ(query)
    def do_POST(self):
        query = {}
        for k, v in parse_qsl(urlparse(self.path)[4]):
            query[k] = v
        for k, v in parse_qsl(self.rfile.read(int(self.headers['Content-Length']))):
            query[k] = v
        self.handleQ(query)
    def log_message(*args): pass # (not needed if nginx is doing it)
    def handleQ(self, query):
        if type("")==type(u"") and type(list(query.keys())[0])==bytes: query=dict((k.decode('utf-8'),v.decode('utf-8')) for k,v in query.items())
        try: req = OpenID.decodeRequest(query)
        except server.ProtocolError as e: return self.encodeAndSend(e)
        if req==None: self.send_response(200),self.end_headers()
        elif req.mode in ["checkid_immediate", "checkid_setup"]: self.checkID(req)
        else: self.encodeAndSend(OpenID.handleRequest(req))
    def checkID(self, req):
        print ("\nGot "+req.mode+" request for "+req.identity+" via "+self.client_address[0]) # (must include client_address to protect against somebody else staging a login to the same site at the same time)
        yn = ''
        while not yn.lower() in ['y','n']:
            print ("Send this ID to "+req.trust_root+"? (y/n): "),
            yn = raw_input()
        if yn.lower()=='y':
            r = req.answer(True,identity=req.identity)
            profile.update({"website":req.identity})
            r.addExtension(sreg.SRegResponse.extractResponse(sreg.SRegRequest.fromOpenIDRequest(req), profile))
        else: r = req.answer(False)
        self.encodeAndSend(r)
        print ("Waiting for new request (Ctrl-C to quit)")
    def encodeAndSend(self, response):
        r = OpenID.encodeResponse(response)
        self.send_response(r.code)
        for h,v in r.headers.items(): self.send_header(h,v)
        self.end_headers()
        if r.body:
            if type(r.body)==type(u""): r.body=r.body.encode('utf-8')
            self.wfile.write(r.body)
httpserver = HTTPServer(local_addr, Handler)
print ("ready for requests (Ctrl-C to quit)")
httpserver.serve_forever()
