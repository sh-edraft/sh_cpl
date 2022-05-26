import unittest

from unittests_cli.add_test_case import AddTestCase
from unittests_cli.build_test_case import BuildTestCase
from unittests_cli.generate_test_case import GenerateTestCase
from unittests_cli.install_test_case import InstallTestCase
from unittests_cli.new_test_case import NewTestCase
from unittests_cli.publish_test_case import PublishTestCase
from unittests_cli.remove_test_case import RemoveTestCase
from unittests_cli.run_test_case import RunTestCase
from unittests_cli.start_test_case import StartTestCase
from unittests_cli.uninstall_test_case import UninstallTestCase
from unittests_cli.update_test_case import UpdateTestCase
from unittests_cli.version_test_case import VersionTestCase


class CLITestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self.addTests(loader.loadTestsFromTestCase(AddTestCase))
        self.addTests(loader.loadTestsFromTestCase(BuildTestCase))
        self.addTests(loader.loadTestsFromTestCase(GenerateTestCase))
        self.addTests(loader.loadTestsFromTestCase(InstallTestCase))
        self.addTests(loader.loadTestsFromTestCase(NewTestCase))
        self.addTests(loader.loadTestsFromTestCase(PublishTestCase))
        self.addTests(loader.loadTestsFromTestCase(RemoveTestCase))
        self.addTests(loader.loadTestsFromTestCase(RunTestCase))
        self.addTests(loader.loadTestsFromTestCase(StartTestCase))
        self.addTests(loader.loadTestsFromTestCase(UninstallTestCase))
        self.addTests(loader.loadTestsFromTestCase(UpdateTestCase))
        self.addTests(loader.loadTestsFromTestCase(VersionTestCase))
