import os
import traceback
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

        self._setup()

        loader = unittest.TestLoader()
        # nothing needed
        self.addTests(loader.loadTestsFromTestCase(GenerateTestCase))
        self.addTests(loader.loadTestsFromTestCase(NewTestCase))
        self.addTests(loader.loadTestsFromTestCase(VersionTestCase))

        # project needed
        self.addTests(loader.loadTestsFromTestCase(BuildTestCase))
        self.addTests(loader.loadTestsFromTestCase(InstallTestCase))
        self.addTests(loader.loadTestsFromTestCase(PublishTestCase))
        self.addTests(loader.loadTestsFromTestCase(RunTestCase))
        self.addTests(loader.loadTestsFromTestCase(StartTestCase))
        self.addTests(loader.loadTestsFromTestCase(UninstallTestCase))
        self.addTests(loader.loadTestsFromTestCase(UpdateTestCase))

        # workspace needed
        self.addTests(loader.loadTestsFromTestCase(AddTestCase))
        self.addTests(loader.loadTestsFromTestCase(RemoveTestCase))

        self._cleanup()

    def _setup(self):
        try:
            playground = os.path.abspath(os.path.join(os.getcwd(), 'test_cli_playground'))
            if os.path.exists(playground):
                os.rmdir(playground)

            os.mkdir(playground)
            os.chdir(playground)
        except Exception as e:
            print(f'Setup of {__name__} failed: {traceback.format_exc()}')

    def _cleanup(self):
        try:
            playground = os.path.abspath(os.path.join(os.getcwd(), 'test_cli_playground'))
            if os.path.exists(playground):
                os.rmdir(playground)
        except Exception as e:
            print(f'Cleanup of {__name__} failed: {traceback.format_exc()}')
