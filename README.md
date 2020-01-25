# CSIRTG-PEERS

The FASTEST way to get the Peers of a an ISP.

# Examples
## Shell
```bash
$ csirtg-peers 1.1.1.1
ipv4
```

## Python
```python
from csirtg_peers import get
from pprint import pprint


for p in get('1.1.1.1'):
    pprint(p)
```

# Before You Begin
If you're using 1.1.1.1 or 8.8.X.X you must set `NAMESERVERS` to a more 'local' nameserver (eg: your ISP).

```shell
$ export NAMESERVER=209.18.47.61
$ csirtg-peers 1.1.1.1
```

This module takes advantage of Team Cymru's IP-ASN Service. 

https://www.team-cymru.com/IP-ASN-mapping.html