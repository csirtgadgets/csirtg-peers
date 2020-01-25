from csirtg_peers import get

IPS = (
    '1.1.1.1',
    '8.8.8.8',
)


def test_basics():
    for i in IPS:
        for p in get(i):
            assert p
