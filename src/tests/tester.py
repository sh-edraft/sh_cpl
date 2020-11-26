import unittest

from tests.logging.logger import LoggerTest
from tests.publishing.publisher import PublisherTest
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
        self._suite.addTest(LoggerTest('test_debug'))
        self._suite.addTest(LoggerTest('test_info'))
        self._suite.addTest(LoggerTest('test_warn'))
        self._suite.addTest(LoggerTest('test_error'))
        self._suite.addTest(LoggerTest('test_fatal'))

        # publishing
        self._suite.addTest(PublisherTest('test_create'))

    def start(self):
        runner = unittest.TextTestRunner()
        runner.run(self._suite)
        # unittest.main()


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
