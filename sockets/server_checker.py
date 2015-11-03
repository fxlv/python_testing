#!/usr/bin/env python
#
# Repeatedly connect to same server to check if it is responding.
# If it does not send a banner, send an HTTP request.
#

# TODO: mesure request latency

import socket
import sys
import time
import datetime

DEFAULT_PORT = 80
DEBUG = False
REQUEST_COUNT = 10

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


def connect(ip, port):
    socket.setdefaulttimeout(1)
    s = socket.socket()

    banner = None
    try:
        if DEBUG: print "Connecting to {}:{}".format(ip, port)
        s.connect((ip, int(port)))
        if DEBUG: print "Connected"
    except Exception, e:
        print "Failed to connect"
        print e
        sys.exit(1)
    if DEBUG: print "Receiving..."
    try:
        banner = s.recv(2048)
    except Exception, e:
        if "timed out" in e:
            if DEBUG: print "Got a timeout, lets try sendig something first"
            if DEBUG: print "Sending 'hi!'..."
            hi = "GET /index.html HTTP/1.1\nUser-Agent: Python/0.01\nHost: {}\nAccept: */*\n\n".format(ip)
            s.send(hi)
            if DEBUG: print "Reveiving..."
            banner = s.recv(2048)
        else:
            if DEBUG: print "Unknown exception"
            if DEBUG: print e
    if banner:
        if DEBUG: print "Banner:\n{}".format(banner)
        if "HTTP/1.1 200 OK" in banner:
            return True
    return False

def main():
    for i in range(1,REQUEST_COUNT):
        now = datetime.datetime.now()
        if connect(ip, port):
            print now, "OK"
            time.sleep(2)
        else:
            print now, "FAIL"
if __name__ == "__main__":
    main()
