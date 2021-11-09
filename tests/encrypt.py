import sys
import unittest

sys.path.append('../sample')
from sample.bilibili import encrypt


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.maxDiff = None
        ret = encrypt(b'''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAx2PrUL06G5oQ1nruhQIX
q1Y3sA41AnhAnOxCyF91JIuaQmKa2zefLvfjDGZVG/UcYvCyIArS99iQurcS6lIT
ROsA1OkVI0F43YS1Xz7v8kALg7qfbtJjO+W0zRYj3dGVA7grwnDNSxdhg2drncb5
qgiPKQ1KefLKV4+hEp6KNh1WpnJXwACQbOTuULIfEp4QA/Ra26H3O5cs+SY4QzE6
Qg026cUqQ14DBXurs3AVzFps0bYQej4SOdg03SuveLFrRyM8IBMhkLLK8zVnaX5B
ZnPEtqbVywVWQuJs6+3vhATfDRNzi97laPwHNfrZvI7mnpJgYxc6xr0RxHNsdLwx
VwIDAQAB
-----END PUBLIC KEY-----''', b'sadsadsadsd')
        self.assertEqual(ret,
                         'KLyiVfFfuZKp7CLqyuGBea_-3VHeZ6f7PUC4D0Cmewfvf2waccv28Wc0IZlUdmd_QZ1FfTWcxBYZK0jalg5HvIMnEhKjg2YMCJTp0Fw1luvV0Dh4FUsJcL2-QmtWCV2-U0yedzXNh7Mw8hVb2jY-obevFNNFTWsnNkG7I8bfSTf8jHnhsbSUcIYtt8AteSWRRlBbCQ4mE_RRsaWi94rmRNpaPDHPM-BgJ7RjokIPkcrPO120KIfMsx42U1M2dgMATFNV1xGQcipLHBFcqVikRxg4lXpB6SE8c7lcsZrPnS9-bVrcu5isHyARnA8v7a7nyME1k-fd-Nh1PUkMWl9q9w')


if __name__ == '__main__':
    unittest.main()
