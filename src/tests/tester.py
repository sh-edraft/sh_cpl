import unittest

from tests.service_provider.service_provider_create import ServiceProviderCreate
from tests.service_provider.service_provider_services import ServiceProviderServices


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()

    def create(self):
        self._suite.addTest(ServiceProviderCreate('test_create'))
        self._suite.addTest(ServiceProviderServices('test_add_singleton'))
        self._suite.addTest(ServiceProviderServices('test_get_singleton'))
        self._suite.addTest(ServiceProviderServices('test_add_scoped'))
        self._suite.addTest(ServiceProviderServices('test_get_scoped'))
        self._suite.addTest(ServiceProviderServices('test_add_transient'))
        self._suite.addTest(ServiceProviderServices('test_get_transient'))

    def start(self):
        unittest.main()


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
