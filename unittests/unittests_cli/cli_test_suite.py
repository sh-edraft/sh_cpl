import os
import shutil
import traceback
import unittest
from typing import Optional
from unittest import TestResult

from unittests_cli.add_test_case import AddTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_cli.generate_test_case import GenerateTestCase
from unittests_cli.install_test_case import InstallTestCase
from unittests_cli.new_test_case import NewTestCase
from unittests_cli.remove_test_case import RemoveTestCase
from unittests_cli.uninstall_test_case import UninstallTestCase


class CLITestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self._result: Optional[TestResult] = None
        # nothing needed
        self.addTests(loader.loadTestsFromTestCase(GenerateTestCase))
        self.addTests(loader.loadTestsFromTestCase(NewTestCase))

        # compare console output
        # self.addTests(loader.loadTestsFromTestCase(VersionTestCase))

        # project needed
        # compare two file states/directory content
        # self.addTests(loader.loadTestsFromTestCase(BuildTestCase))

        self.addTests(loader.loadTestsFromTestCase(InstallTestCase))

        # compare two file states/directory content
        # self.addTests(loader.loadTestsFromTestCase(PublishTestCase))

        # check if application was executed properly
        # self.addTests(loader.loadTestsFromTestCase(RunTestCase))

        # check if application was executed properly and file watcher is working
        # self.addTests(loader.loadTestsFromTestCase(StartTestCase))

        self.addTests(loader.loadTestsFromTestCase(UninstallTestCase))

        # check in project settings if package is updated
        # self.addTests(loader.loadTestsFromTestCase(UpdateTestCase))

        # workspace needed
        self.addTests(loader.loadTestsFromTestCase(AddTestCase))
        self.addTests(loader.loadTestsFromTestCase(RemoveTestCase))

    def _setup(self):
        try:
            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH)))

            os.makedirs(PLAYGROUND_PATH)
            os.chdir(PLAYGROUND_PATH)
        except Exception as e:
            print(f'Setup of {__name__} failed: {traceback.format_exc()}')

    def _cleanup(self):
        try:
            if self._result is not None and (len(self._result.errors) > 0 or len(self._result.failures) > 0):
                return

            if os.path.exists(PLAYGROUND_PATH):
                shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH)))
        except Exception as e:
            print(f'Cleanup of {__name__} failed: {traceback.format_exc()}')

    def run(self, *args):
        self._setup()
        self._result = super().run(*args)
        self._cleanup()
