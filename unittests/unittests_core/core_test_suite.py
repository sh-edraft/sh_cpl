import unittest

from unittests_core.configuration.console_arguments_test_case import ConsoleArgumentsTestCase
from unittests_core.configuration.configuration_test_case import ConfigurationTestCase
from unittests_core.configuration.environment_test_case import EnvironmentTestCase
from unittests_core.di.service_collection_test_case import ServiceCollectionTestCase
from unittests_core.di.service_provider_test_case import ServiceProviderTestCase
from unittests_core.pipes.bool_pipe_test_case import BoolPipeTestCase
from unittests_core.pipes.ip_address_pipe_test_case import IPAddressTestCase
from unittests_core.pipes.version_pipe_test_case import VersionPipeTestCase
from unittests_core.utils.credential_manager_test_case import CredentialManagerTestCase
from unittests_core.utils.json_processor_test_case import JSONProcessorTestCase
from unittests_core.utils.string_test_case import StringTestCase


class CoreTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        tests = [
            # config
            ConfigurationTestCase,
            ConsoleArgumentsTestCase,
            EnvironmentTestCase,
            # di
            ServiceCollectionTestCase,
            ServiceProviderTestCase,
            # pipes
            BoolPipeTestCase,
            IPAddressTestCase,
            VersionPipeTestCase,
            # utils
            CredentialManagerTestCase,
            JSONProcessorTestCase,
            StringTestCase,
        ]

        for test in tests:
            self.addTests(loader.loadTestsFromTestCase(test))

    def run(self, *args):
        super().run(*args)


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(CoreTestSuite())
