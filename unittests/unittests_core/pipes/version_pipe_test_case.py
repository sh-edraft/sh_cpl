import unittest

from cpl_core.pipes.version_pipe import VersionPipe


class VersionPipeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_transform(self):
        pipe = VersionPipe()

        self.assertEqual("1.1.1", pipe.transform({"Major": 1, "Minor": 1, "Micro": 1}))
        self.assertEqual("0.1.1", pipe.transform({"Major": 0, "Minor": 1, "Micro": 1}))
        self.assertEqual("0.0.1", pipe.transform({"Major": 0, "Minor": 0, "Micro": 1}))
        self.assertEqual("0.0.0", pipe.transform({"Major": 0, "Minor": 0, "Micro": 0}))
