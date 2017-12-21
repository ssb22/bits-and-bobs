#!/usr/bin/env python

print "OpenID Command-line Authoriser v1.1, Silas S. Brown 2017 (public domain)\n"

from openid_config import local_addr, public_endpoint_url, profile

import sys
try: import openid
except ImportError: sys.stderr.write("Library not found\nTry: sudo apt-get install python-openid\n"),sys.exit(1)
print "Make sure your home page <head> section has:"
print '<link rel="openid.server" href="'+public_endpoint_url+'" />\n'
print "Loading...", ; sys.stdout.flush()
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse
from cgi import parse_qsl
from openid.server import server
from openid.store.memstore import MemoryStore
from openid.extensions import sreg
OpenID = server.Server(MemoryStore(), public_endpoint_url)
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
        try: req = OpenID.decodeRequest(query)
        except server.ProtocolError, e: return self.encodeAndSend(e)
        if req==None: self.send_response(200),self.end_headers()
        elif req.mode in ["checkid_immediate", "checkid_setup"]: self.checkID(req)
        else: self.encodeAndSend(OpenID.handleRequest(req))
    def checkID(self, req):
        print "\nGot",req.mode,"request for",req.identity,"via",self.client_address[0] # (must include client_address to protect against somebody else staging a login to the same site at the same time)
        yn = ''
        while not yn.lower() in ['y','n']:
            print "Send this ID to "+req.trust_root+"? (y/n): ",
            yn = raw_input()
        if yn.lower()=='y':
            r = req.answer(True,identity=req.identity)
            profile.update({"website":req.identity})
            r.addExtension(sreg.SRegResponse.extractResponse(sreg.SRegRequest.fromOpenIDRequest(req), profile))
        else: r = req.answer(False)
        self.encodeAndSend(r)
    def encodeAndSend(self, response):
        r = OpenID.encodeResponse(response)
        self.send_response(r.code)
        for h,v in r.headers.iteritems(): self.send_header(h,v)
        self.end_headers()
        if r.body: self.wfile.write(r.body)
httpserver = HTTPServer(local_addr, Handler)
print "ready for requests (Ctrl-C to quit)"
httpserver.serve_forever()
