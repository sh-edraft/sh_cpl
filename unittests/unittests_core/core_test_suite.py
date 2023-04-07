import unittest

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
