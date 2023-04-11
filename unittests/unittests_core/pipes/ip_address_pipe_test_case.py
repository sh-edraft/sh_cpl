import unittest

from cpl_core.pipes import IPAddressPipe


class IPAddressTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_transform(self):
        pipe = IPAddressPipe()

        self.assertEqual("192.168.178.1", pipe.transform([192, 168, 178, 1]))
        self.assertEqual("255.255.255.255", pipe.transform([255, 255, 255, 255]))
        self.assertEqual("0.0.0.0", pipe.transform([0, 0, 0, 0]))

        self.assertRaises(Exception, lambda: pipe.transform([-192, 168, 178, 1]))
        self.assertRaises(Exception, lambda: pipe.transform([256, 168, 178, 1]))
        self.assertRaises(Exception, lambda: pipe.transform([256, 168, 178]))
        self.assertRaises(Exception, lambda: pipe.transform([256, 168, 178, 1, 1]))
