import unittest

from tests.configuration.config import ConfigTest
from tests.hosting.app_host import AppHostTest
from tests.services.logging.logger import LoggerTest
from tests.services.publishing.publisher import PublisherTest
from tests.service_providing.service_provider import ServiceProviderTest


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()

    def create(self):
        # hosting app host
        self._suite.addTest(AppHostTest('test_create'))

        # configuration
        self._suite.addTest(ConfigTest('test_create'))
        self._suite.addTest(ConfigTest('test_env_vars'))
        self._suite.addTest(ConfigTest('test_arguments'))
        self._suite.addTest(ConfigTest('test_appsettings'))
        self._suite.addTest(ConfigTest('test_appsettings_environment'))
        self._suite.addTest(ConfigTest('test_appsettings_host'))
        self._suite.addTest(ConfigTest('test_appsettings_customer'))

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
