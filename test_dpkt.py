#!/usr/bin/env python
"""
Use DPKT to read in a pcap file and print out the contents of the packets
This example is focused on the fields in the Ethernet Frame and IP packet
"""
import dpkt
import datetime
import socket
from ipaddress import ip_address


def mac_addr(address):
    """Convert a MAC address to a readable/printable string

       Args:
           address (str): a MAC address in hex form (e.g. '\x01\x02\x03\x04\x05\x06')
       Returns:
           str: Printable/readable MAC address
    """
    return ':'.join('%02x' % ord(b) for b in address)



def ip_to_str(address):
    """Print out an IP address given a string

    Args:
        address (inet struct): inet network address
    Returns:
        str: Printable/readable IP address
    """
    return socket.inet_ntop(socket.AF_INET, address)



def print_packets(pcap):
    f = open('capture.txt', 'w')
    """Print out information about each packet in a pcap

       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Print out the timestamp in UTC
        f.write('Timestamp: %s \n'%str(datetime.datetime.utcfromtimestamp(timestamp)))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        d = 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type
        f.write(str(d))

        # Make sure the Ethernet frame contains an IP packet
        # EtherType (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
        print dpkt.icmp6.ICMP6_ECHO_REQUEST
        if eth.type != dpkt.ethernet.ETH_TYPE_IP or eth.type != dpkt.ethernet.ETH_TYPE_IP6:
            ip = eth.data
            data = ip.data
            data2 = data.data
            print ip_address(ip.src)
            print ip_address(ip.dst)
            print data.type


            if data.type in [127, 128, 129, 138]:
                print data.type
            f.write('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Now unpack the data within the Ethernet frame (the IP packet)
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the info


        f.write( 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
                (ip_to_str(ip.src), ip_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset))



def test():
    """Open up a test pcap file and print out the packets"""
    with open('benign.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        print_packets(pcap)



if __name__ == '__main__':
    test()
