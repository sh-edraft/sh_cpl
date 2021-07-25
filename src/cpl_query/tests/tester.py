import unittest

from cpl_query.tests.query_test import QueryTest


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()

    def create(self):
        loader = unittest.TestLoader()
        self._suite.addTests(loader.loadTestsFromTestCase(QueryTest))

    def start(self):
        runner = unittest.TextTestRunner()
        runner.run(self._suite)


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
