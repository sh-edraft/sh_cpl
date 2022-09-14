import unittest

from unittests_query.enumerable_query_test_case import EnumerableQueryTestCase
from unittests_query.enumerable_test_case import EnumerableTestCase
from unittests_query.iterable_query_test_case import IterableQueryTestCase
from unittests_query.iterable_test_case import IterableTestCase
from unittests_query.sequence_test_case import SequenceTestCase


class QueryTestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(SequenceTestCase))
        self.addTests(loader.loadTestsFromTestCase(EnumerableTestCase))
        self.addTests(loader.loadTestsFromTestCase(EnumerableQueryTestCase))
        self.addTests(loader.loadTestsFromTestCase(IterableTestCase))
        self.addTests(loader.loadTestsFromTestCase(IterableQueryTestCase))

    def run(self, *args):
        super().run(*args)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(QueryTestSuite())