#!/usr/bin/env python
import socket
import sys

DEFAULT_PORT = 22

def usage():
    print "Usage:"
    print "{} <ip:port>".format(sys.argv[0])
    print
    sys.exit(0)

try:
    target = sys.argv[1]
    if len(target.split(":")) == 2:
        ip, port = target.split(":")
    else:
        ip = target
        port = DEFAULT_PORT
except:
    usage()

socket.setdefaulttimeout(1)
s = socket.socket()

banner = None
try:
    s.connect((ip, int(port)))
    print "Connected"
except Exception, e:
    print "Failed to connect"
    print e
    sys.exit(1)
print "Receiving..."
try:
    banner = s.recv(2048)
except Exception, e:
    if "timed out" in e:
        print "Got a timeout, lets try sendig something first"
        print "Sending 'hi!'..."
        s.send("hi!")
        print "Reveiving..."
        banner = s.recv(2048)
    else:
        print "Unknown exception"
        print e
if banner:
    print "Banner:\n{}".format(banner)
