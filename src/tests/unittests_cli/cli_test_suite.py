import os
import shutil
import traceback
import unittest

from unittests_cli.add_test_case import AddTestCase
from unittests_cli.build_test_case import BuildTestCase
from unittests_cli.constants import PLAYGROUND_PATH
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

    def _setup(self):
        print(f'Setup {__name__}')
        try:
            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(PLAYGROUND_PATH)

            os.mkdir(PLAYGROUND_PATH)
            os.chdir(PLAYGROUND_PATH)
        except Exception as e:
            print(f'Setup of {__name__} failed: {traceback.format_exc()}')

    def _cleanup(self):
        print(f'Cleanup {__name__}')
        try:
            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(PLAYGROUND_PATH)
        except Exception as e:
            print(f'Cleanup of {__name__} failed: {traceback.format_exc()}')

    def run(self, *args):
        self._setup()
        super().run(*args)
        self._cleanup()
