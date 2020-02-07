import re
import os
import dns.resolver
from dns.resolver import NoAnswer, NXDOMAIN, NoNameservers, Timeout
from dns.name import EmptyLabel

from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

RE_IP = re.compile('^(\S+)\/\d+$')

NAMESERVER = os.getenv('NAMESERVER')

TIMEOUT = 5


def _get(data, t='TXT', timeout=TIMEOUT, nameserver=NAMESERVER):
    resolver = dns.resolver.Resolver()
    resolver.timeout = timeout
    resolver.lifetime = timeout
    resolver.search = []

    if nameserver:
        resolver.nameservers = [nameserver]

    try:
        answers = resolver.query(data, t)

    except (NoAnswer, NXDOMAIN, EmptyLabel, NoNameservers, Timeout) as e:
        e = str(e)
        if e.startswith('The DNS operation timed out after'):
            return

        if 'The DNS response does not contain' in e or \
                'None of DNS query names exist' in e:
            return

        raise

    for rdata in answers:
        yield rdata


def get(ip: str) -> dict:
    """Lookup PEERS for an ip address

Example:

    from pprint import pprint
    for p in get_peers('1.1.1.1'):
        pprint(p)

    {'asn': '174', 'cc': 'US', 'prefix': '128.205.0.0/16', 'rir': 'arin'}
    {'asn': '3356', 'cc': 'US', 'prefix': '128.205.0.0/16', 'rir': 'arin'}
    {'asn': '3630', 'cc': 'US', 'prefix': '128.205.0.0/16', 'rir': 'arin'}
    {'asn': '3754', 'cc': 'US', 'prefix': '128.205.0.0/16', 'rir': 'arin'}

Args:

    :param ip: ip address

Returns:

    :rtype: generator of dicts
    """
    match = RE_IP.search(ip)
    if match:
        ip = match.group(1)

    # cache it to the /24
    ip = list(reversed(ip.split('.')))

    # Separate fields and order by netmask length
    # 23028 | 216.90.108.0/24 | US | arin | 1998-09-25
    # 701 1239 3549 3561 7132 | 216.90.108.0/24 | US | arin | 1998-09-25
    for p in _get(f"0.{ip[1]}.{ip[2]}.{ip[3]}.peer.asn.cymru.com"):
        bits = str(p).replace('"', '').strip().split(' | ')

        try:
            asn, prefix, cc, rir, _ = bits

        except ValueError:
            asn, prefix, cc, rir = bits

        asns = asn.split(' ')
        for a in asns:
            yield {
                'asn': a,
                'prefix': prefix,
                'cc': cc,
                'rir': rir
            }


def main():  # pragma: no cover
    import sys
    from pprint import pprint

    i = sys.argv[1]

    for p in get(i):
        pprint(p)


if __name__ == "__main__":  # pragma: no cover
    main()
