import unittest
from unittest import TestSuite

from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC
from unittests.test_case import TestCase


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)
        self._suite: TestSuite = unittest.TestSuite()

    def configure(self):
        self._suite.addTest(TestCase('test_equal'))

    def main(self):
        runner = unittest.TextTestRunner()
        runner.run(self._suite)
