import unittest

from unittests_core.utils.string_test_case import StringTestCase


class CoreTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(StringTestCase))

    def run(self, *args):
        super().run(*args)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(CoreTestSuite())
