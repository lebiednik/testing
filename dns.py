import collections
import functools
from ipaddress import ip_address

import dpkt

from .base import PacketHandler, Unicode

# DNS Type Decoding: https://www.iana.org/assignments/dns-parameters
DNS_RR_TYPES = {
    1: "A",
    2: "NS",
    3: "MD",
    4: "MF",
    5: "CNAME",
    6: "SOA",
    7: "MB",
    8: "MG",
    9: "MR",
    10: "NULL",
    11: "WKS",
    12: "PTR",
    13: "HINFO",
    14: "MINFO",
    15: "MX",
    16: "TXT",
    17: "RP",
    18: "AFSDB",
    19: "X25",
    20: "ISDN",
    21: "RT",
    22: "NSAP",
    23: "NSAP-PTR",
    24: "SIG",
    25: "KEY",
    26: "PX",
    27: "GPOS",
    28: "AAAA",
    29: "LOC",
    30: "NXT",
    31: "EID",
    32: "NIMLOC",
    33: "SRV",
    34: "ATMA",
    35: "NAPTR",
    36: "KX",
    37: "CERT",
    38: "A6",
    39: "DNAME",
    40: "SINK",
    41: "OPT",
    42: "APL",
    43: "DS",
    44: "SSHFP",
    45: "IPSECKEY",
    46: "RRSIG",
    47: "NSEC",
    48: "DNSKEY",
    49: "DHCID",
    50: "NSEC3",
    51: "NSEC3PARAM",
    55: "HIP",
    56: "NINFO",
    57: "RKEY",
    58: "TALINK",
    59: "CDS",
    99: "SPF",
    100: "UINFO",
    101: "UID",
    102: "GID",
    103: "UNSPEC",
    249: "TKEY",
    250: "TSIG",
    251: "IXFR",
    252: "AXFR",
    253: "MAILB",
    254: "MAILA",
    255: "*",
    256: "URI",
    257: "CAA",
    32768: "TA",
    65535: "Reserved",
}

DNS_RCODE = {
    0: "NOERR",
    1: "FORMERR",
    2: "SERVFAIL",
    3: "NXDOMAIN",
    4: "NOTIMP",
    5: "REFUSED",
    6: "YXDOMAIN",
    7: "YXRRSET",
    8: "NXRRSET",
    9: "NOTAUTH",
    10: "NOTZONE",
}

def handle(data, dport, sport, dns_info, dns_session, logger):
    """Handle both TCP and UDP DNS requests"""
    # Create this handler to parse both --remove
    if dport == 53 or sport == 53:
        try:
            dns = dpkt.dns.DNS(data)  # change udp.data --remove
        except Exception:
            self.logger.debug('Exception parsing DNS', exc_info=True)
            return False
        if dns.opcode != dpkt.dns.DNS_QUERY:
            # Currently only handle standard queries
            return True

        if forward:
            server_ip = ip_address(ip.dst)
            client_port = sport
        else:
            server_ip = ip_address(ip.src)
            client_port = dport

        if dns.qr == dpkt.dns.DNS_Q:
            handle_query(ts, dns, server_ip, client_port, netflow)
            # Add this to global --remove
        else:
            handle_answer(ts, dns, server_ip, client_port, netflow)
            # Add this to global --remove

        return True
    return False



class DNSUDPHandler(PacketHandler):
    protocol = 'dns'

    def __init__(self, *args, **kwargs):
        super(DNSUDPHandler, self).__init__(*args, **kwargs)

        self.queries = collections.OrderedDict()

    @staticmethod
    def dns_name(name):
        return Unicode(name, ['idna', 'latin-1']).lower()

    def parse_dns_question(self, dns, ts, netflow):
        if len(dns.qd) != 1:
            self.logger.warn("Don't currently support multiple questions")
            return None

        q = dns.qd[0]
        if q.cls != dpkt.dns.DNS_IN:
            # Ignore non-Internet Protocol requests
            return None

        rname = self.dns_name(q.name)
        rtype = DNS_RR_TYPES.get(q.type, unicode(q.type))

        return {
            'time': ts,
            'type': rtype,
            'name': rname,
            'netflow': netflow,
            'rcode': None,
            'answers': [],
            'authorities': [],
            'additional': [],
        }

    def parse_dns_rr(self, rr):
        rtype = DNS_RR_TYPES.get(rr.type, unicode(rr.type))
        answer = {
            'name': self.dns_name(rr.name),
            'type': rtype,
            'ttl': rr.ttl,
        }

        handlers = {
            'A': [('ip', 'ip', ip_address)],
            'AAAA': [('ip', 'ip6', ip_address)],
            'NS': [('rname', 'nsname', self.dns_name)],
            'CNAME': [('rname', 'cname', self.dns_name)],
            'PTR': [('rname', 'ptrname', self.dns_name)],
            'SOA': [('rname', 'mname', self.dns_name)],
            'MX': [('rname', 'mxname', self.dns_name),
                   ('priority', 'preference', int)],
            # TODO: The so-called "text" field actually contains arbitrary
            # binary data.  For the moment, we'll just throw it through
            # UnicodeDammit.
            'TXT': [('text', 'text', functools.partial(map, Unicode))],
            'HINFO': [('text', 'text', functools.partial(map, Unicode))],
            'SRV': [('rname', 'srvname', self.dns_name),
                    ('priority', 'priority', int),
                    ('port', 'port', int)],
        }

        for dst, src, cast in handlers.get(rtype, []):
            answer[dst] = cast(getattr(rr, src))

        return answer

    def handle_query(self, ts, dns, server_ip, client_port, netflow):
        key = (server_ip, client_port, dns.id)
        # This is a DNS query
        if key in self.queries:
            # TODO: Assert that this query is the same as the previous one.
            return
        question = self.parse_dns_question(dns, ts, netflow)
        if question:
            question['server'] = server_ip
            self.queries[key] = question

    def handle_answer(self, ts, dns, server_ip, client_port, netflow):
        key = (server_ip, client_port, dns.id)
        dns_entry = self.queries.get(key)
        if dns_entry is None:
            dns_entry = self.parse_dns_question(dns, ts, netflow)
            if dns_entry:
                dns_entry['server'] = server_ip
                self.queries[key] = dns_entry
            else:
                return
        dns_entry['rcode'] = DNS_RCODE.get(dns.rcode, unicode(dns.rcode))
        for rr in dns.an:
            # Answers
            dns_entry['answers'].append(self.parse_dns_rr(rr))
        for rr in dns.ns:
            # Authorities
            dns_entry['authorities'].append(self.parse_dns_rr(rr))
        for rr in dns.ar:
            # Additional information
            dns_entry['additional'].append(self.parse_dns_rr(rr))

    def handle(self, ts, pkt, forward, netflow):
        ip = pkt.data
        udp = ip.udp
        return handle(udp.data, udp.dport, udp.sport, info, self.dns_session, self.logger)
        """if (forward and udp.dport == 53) or (not forward and udp.sport == 53):
            try:
                dns = dpkt.dns.DNS(udp.data)
            except Exception:
                self.logger.debug('Exception parsing DNS', exc_info=True)
                return False
        --remove

            if dns.opcode != dpkt.dns.DNS_QUERY:
                # Currently only handle standard queries
                return True

            if forward:
                server_ip = ip_address(ip.dst)
                client_port = udp.sport
            else:
                server_ip = ip_address(ip.src)
                client_port = udp.dport

            if dns.qr == dpkt.dns.DNS_Q:
                self.handle_query(ts, dns, server_ip, client_port, netflow)
            else:
                self.handle_answer(ts, dns, server_ip, client_port, netflow)

            return True
        return False
        """

    def finish(self):
        return list(self.queries.values())


class DNSTCPHandler(StreamHandler):
    # changed the names and super names --remove
    protocol = 'dns'

    def __init__(self, *args, **kwargs):
        super(DNSTCPHandler, self).__init__(*args, **kwargs)

        self.queries = collections.OrderedDict()

    @staticmethod
    def dns_name(name):
        return Unicode(name, ['idna', 'latin-1']).lower()

    def parse_dns_question(self, dns, ts, netflow):
        if len(dns.qd) != 1:
            self.logger.warn("Don't currently support multiple questions")
            return None

        q = dns.qd[0]
        if q.cls != dpkt.dns.DNS_IN:
            # Ignore non-Internet Protocol requests
            return None

        rname = self.dns_name(q.name)
        rtype = DNS_RR_TYPES.get(q.type, unicode(q.type))

        return {
            'time': ts,
            'type': rtype,
            'name': rname,
            'netflow': netflow,
            'rcode': None,
            'answers': [],
            'authorities': [],
            'additional': [],
        }

    def parse_dns_rr(self, rr):
        rtype = DNS_RR_TYPES.get(rr.type, unicode(rr.type))
        answer = {
            'name': self.dns_name(rr.name),
            'type': rtype,
            'ttl': rr.ttl,
        }

        handlers = {
            'A': [('ip', 'ip', ip_address)],
            'AAAA': [('ip', 'ip6', ip_address)],
            'NS': [('rname', 'nsname', self.dns_name)],
            'CNAME': [('rname', 'cname', self.dns_name)],
            'PTR': [('rname', 'ptrname', self.dns_name)],
            'SOA': [('rname', 'mname', self.dns_name)],
            'MX': [('rname', 'mxname', self.dns_name),
                   ('priority', 'preference', int)],
            # TODO: The so-called "text" field actually contains arbitrary
            # binary data.  For the moment, we'll just throw it through
            # UnicodeDammit.
            'TXT': [('text', 'text', functools.partial(map, Unicode))],
            'HINFO': [('text', 'text', functools.partial(map, Unicode))],
            'SRV': [('rname', 'srvname', self.dns_name),
                    ('priority', 'priority', int),
                    ('port', 'port', int)],
        }

        for dst, src, cast in handlers.get(rtype, []):
            answer[dst] = cast(getattr(rr, src))

        return answer

    def handle_query(self, ts, dns, server_ip, client_port, netflow):
        key = (server_ip, client_port, dns.id)
        # This is a DNS query
        if key in self.queries:
            # TODO: Assert that this query is the same as the previous one.
            return
        question = self.parse_dns_question(dns, ts, netflow)
        if question:
            question['server'] = server_ip
            self.queries[key] = question

    def handle_answer(self, ts, dns, server_ip, client_port, netflow):
        key = (server_ip, client_port, dns.id)
        dns_entry = self.queries.get(key)
        if dns_entry is None:
            dns_entry = self.parse_dns_question(dns, ts, netflow)
            if dns_entry:
                dns_entry['server'] = server_ip
                self.queries[key] = dns_entry
            else:
                return
        dns_entry['rcode'] = DNS_RCODE.get(dns.rcode, unicode(dns.rcode))
        for rr in dns.an:
            # Answers
            dns_entry['answers'].append(self.parse_dns_rr(rr))
        for rr in dns.ns:
            # Authorities
            dns_entry['authorities'].append(self.parse_dns_rr(rr))
        for rr in dns.ar:
            # Additional information
            dns_entry['additional'].append(self.parse_dns_rr(rr))

    def handle(self, sockpair, flow, netflow, tcpflow):
        # worked first 4 lines  --remove
        forward = flow.fwd.data
        sport = sockpair[0][1]
        dport = sockpair[1][1]
        # return handle(forward, dport, sport, info, self.dns_session, self.logger)
        """if (forward and dport == 53) or (not forward and sport == 53):
            try:
                dns = dpkt.dns.DNS(udp.data)
            except Exception:
                self.logger.debug('Exception parsing DNS', exc_info=True)
                return False
        --remove

            if dns.opcode != dpkt.dns.DNS_QUERY:
                # Currently only handle standard queries
                return True

            if forward:
                server_ip = ip_address(ip.dst)
                client_port = sport
            else:
                server_ip = ip_address(ip.src)
                client_port = dport

            if dns.qr == dpkt.dns.DNS_Q:
                self.handle_query(ts, dns, server_ip, client_port, netflow)
            else:
                self.handle_answer(ts, dns, server_ip, client_port, netflow)

            return True
        return False
        """

    def finish(self):
        return list(self.queries.values())
