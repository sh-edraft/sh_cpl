import unittest

from cpl_core.utils.json_processor import JSONProcessor


class SubTestClass:
    def __init__(self, value: str = None):
        self.value = value


class TestClass:
    def __init__(self, i: int = None, s: str = None, d: dict = None, l: list = None, value: SubTestClass = None):
        self.i = i
        self.s = s
        self.d = d
        self.l = l
        self.value = value


class JSONProcessorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_process(self):
        test_dict = {
            "i": 10,
            "s": "Hello World",
            "d": {"test": "Test"},
            "l": range(0, 11),
            "value": {"value": "Hello World"},
        }
        test: TestClass = JSONProcessor.process(TestClass, test_dict)

        self.assertEqual(test.i, test_dict["i"])
        self.assertEqual(test.s, test_dict["s"])
        self.assertEqual(test.d, test_dict["d"])
        self.assertEqual(test.l, test_dict["l"])
        self.assertEqual(test.value.value, test_dict["value"]["value"])
