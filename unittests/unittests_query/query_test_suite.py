import unittest

from unittests_query.iterable_test_case import IterableTestCase
from unittests_query.query_test_case import QueryTestCase


class QueryTestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(QueryTestCase))
        self.addTests(loader.loadTestsFromTestCase(IterableTestCase))

    def run(self, *args):
        super().run(*args)
