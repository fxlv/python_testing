#!/usr/bin/env python
import socket
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("target", help="Target. IP or hostname.")
parser.add_argument("ports", help="Target ports (comma separated)")
args = parser.parse_args()

target = args.target
ports = args.ports

# support specifying multiple comma separated ports
if len(ports.split(",")) > 0:
    ports = ports.split(",")
else:
    ports = [ports]

print "Target: {}, ports: {}".format(target, str(ports))


def grab(target, port):
    banner = None
    socket.setdefaulttimeout(1)
    s = socket.socket()
    try:
        s.connect((target, int(port)))
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


def main():
    for port in ports:
        grab(target, port)


if __name__ == "__main__":
    main()
