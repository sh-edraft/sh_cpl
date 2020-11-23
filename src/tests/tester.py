import unittest

from tests.logging.logger import LoggerTest
from tests.service_providing.service_provider import ServiceProviderTest


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()

    def create(self):
        # providing
        self._suite.addTest(ServiceProviderTest('test_create'))
        self._suite.addTest(ServiceProviderTest('test_add_singleton'))
        self._suite.addTest(ServiceProviderTest('test_get_singleton'))
        self._suite.addTest(ServiceProviderTest('test_add_scoped'))
        self._suite.addTest(ServiceProviderTest('test_get_scoped'))
        self._suite.addTest(ServiceProviderTest('test_add_transient'))
        self._suite.addTest(ServiceProviderTest('test_get_transient'))

        # logging
        self._suite.addTest(LoggerTest('test_create'))
        self._suite.addTest(LoggerTest('test_header'))
        self._suite.addTest(LoggerTest('test_trace'))

        # publishing

    def start(self):
        unittest.main()


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
