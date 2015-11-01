#!/usr/bin/env python

import socket
import time
import sys

def sleepy(seconds):
    print "Sleeping for {} seconds".format(seconds),
    while seconds > 0:
        print ".",
        sys.stdout.flush()
        time.sleep(1)
        seconds = seconds - 1
    print " done."

def main():
    if len(sys.argv) == 2:
        endpoint = sys.argv[1]
    else:
        endpoint = 'fxtcptest.cloudapp.net'

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((endpoint, 22330))

    print "Using endpoint {}".format(endpoint)
    # initial sleep time = 2 mins
    sleep_time = 240
    while True:
        try:
            client.send("ping")
            print "Ping sent"
            sleepy(sleep_time)
        except socket.error:
            print "Socket error ocurred after a {} second sleep time".format(sleep_time)
            sys.exit(0)
        sleep_time += 20

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
        print "Exiting..."
