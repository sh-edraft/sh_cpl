import unittest

from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC
from unittests_cli.cli_test_suite import CLITestSuite
from unittests_query.query_test_suite import QueryTestSuite


class Application(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

    def configure(self):
        pass

    def main(self):
        runner = unittest.TextTestRunner()
        runner.run(CLITestSuite())
        runner.run(QueryTestSuite())
