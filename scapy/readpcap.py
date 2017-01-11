#!/usr/bin/env python
from scapy.all import *
import argparse
import os
import sys
import ipdb

class Flow:
    """
    Flow is a unique collection of:
    src:srcport -> dst:dstport protocol
    """

    def __init__(self, packet, src, dst, sport=None, dport=None, proto=None):
        self.src = src
        self.dst = dst
        self.sport = sport
        self.dport = dport
        self.proto = proto
        self.packets = []
        self.packets.append(packet)
        self.hash = self.calculate_hash(self.proto, self.src, self.sport, self.dst, self.dport)

    def __str__(self):
        if self.dport and self.sport:
            str = "{} {}:{} -> {}:{}".format(self.proto, self.src, self.sport, self.dst, self.dport)
        else:
            str = "{} -> {}".format(self.src, self.dst)
        return str

    def __repr__(self):
        return "Flow({})".format(self.__str__())

    def __len__(self):
        return len(self.packets)

    def calculate_hash(*args):
        string = ""
        for arg in args:
            string += str(arg)
        return hashlib.sha256(string).hexdigest()

def analyze(packet):
    """Analyzes PCAP packet and returns a Flow() object."""
    proto = None
    sport = None
    dport = None
    if packet.haslayer(IP):
        # we skip Ethernet and go directly to IP
        packet = packet.getlayer(IP)
        src, dst = packet.src, packet.dst
        if packet.haslayer(TCP):
            proto = "TCP"
            packet = packet.getlayer(TCP)
            dport, sport = packet.dport, packet.sport
        elif packet.haslayer(UDP):
            proto = "UDP"
            packet = packet.getlayer(UDP)
            dport, sport = packet.dport, packet.sport
        return Flow(packet, src, dst, sport, dport, proto)
    else:
        # TODO: handle this better
        print "No IP layer: ",packet
        return False


def die(msg):
    print msg
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap-file", required=True)
    args = parser.parse_args()
    return args


def read_pcap(pcap_file):
    if not os.path.exists(pcap_file):
        die("Pcap file missing")
    return rdpcap(pcap_file)



def analyze_all(capture):
    flows = {}
    for packet in capture:
        flow = analyze(packet)
        if not flow:
            continue  # ignore invalid packets
        if flow.hash in flows:
            flows[flow.hash].packets.append(packet)
        else:
            flows[flow.hash] = flow
    return flows

def print_all(flows):
    for flow in flows:
        print flows[flow], len(flows[flow])


def main():
    args = parse_args()
    flows = analyze_all(read_pcap(args.pcap_file))
    print_all(flows)

if __name__ == "__main__":
    main()
