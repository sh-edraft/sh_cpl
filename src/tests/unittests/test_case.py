import unittest


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_equal(self):
        self.assertEqual(True, True)
