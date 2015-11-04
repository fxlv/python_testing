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
import argparse


DEBUG = False
def connect(target, port):
    socket.setdefaulttimeout(1)
    s = socket.socket()

    banner = None
    try:
        if DEBUG: print "Connecting to {}:{}".format(target, port)
        s.connect((target, int(port)))
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
            hi = "GET /index.html HTTP/1.1\nUser-Agent: Python/0.01\nHost: {}\nAccept: */*\n\n".format(target)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("port", type=int, help="Target port")
    parser.add_argument("-c", default=1, type=int, help="Request count")
    parser.add_argument("-s",  default=1, type=int, help="Sleep time between retries (seconds)")
    args = parser.parse_args()

    target = args.target
    port = args.port
    count = args.c
    sleep_time = args.s
    print "Target: {}, port: {}, connect count: {}".format(target, port, count)
    for i in range(0,count):
        now = datetime.datetime.now()
        if connect(target, port):
            print now, "OK"
        else:
            print now, "FAIL"
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
