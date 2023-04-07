import unittest

from unittests_core.utils.string_test_case import StringTestCase
from unittests_query.enumerable_query_test_case import EnumerableQueryTestCase
from unittests_query.enumerable_test_case import EnumerableTestCase
from unittests_query.iterable_query_test_case import IterableQueryTestCase
from unittests_query.iterable_test_case import IterableTestCase
from unittests_query.sequence_test_case import SequenceTestCase


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
