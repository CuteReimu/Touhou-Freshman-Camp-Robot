import base64
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.maxDiff = None
        self.assertEqual(b'_zI',
                         base64.urlsafe_b64encode(b'\xff2').rstrip(b'='))


if __name__ == '__main__':
    unittest.main()
