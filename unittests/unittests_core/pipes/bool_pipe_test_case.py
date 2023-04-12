import unittest

from cpl_core.pipes import BoolPipe


class BoolPipeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_transform(self):
        pipe = BoolPipe()

        self.assertEqual("True", pipe.transform(True))
        self.assertEqual("False", pipe.transform(False))
