import os
import shutil
import traceback
import unittest
from typing import Optional
from unittest import TestResult

from unittests_cli.add_test_case import AddTestCase
from unittests_cli.build_test_case import BuildTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_cli.generate_test_case import GenerateTestCase
from unittests_cli.install_test_case import InstallTestCase
from unittests_cli.new_test_case import NewTestCase
from unittests_cli.publish_test_case import PublishTestCase
from unittests_cli.remove_test_case import RemoveTestCase
from unittests_cli.run_test_case import RunTestCase
from unittests_cli.uninstall_test_case import UninstallTestCase
from unittests_cli.update_test_case import UpdateTestCase


class CLITestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self._result: Optional[TestResult] = None
        self._is_online = True

        active_tests = [
            # nothing needed
            GenerateTestCase,
            NewTestCase,
            # compare console output
            # VersionTestCase,
            # project needed
            BuildTestCase,
            PublishTestCase,
            RunTestCase,
            # check if application was executed properly and file watcher is working
            # StartTestCase,
            # check in project settings if package is updated
            # UpdateTestCase,
            # workspace needed
            AddTestCase,
            RemoveTestCase
        ]

        if self._is_online:
            active_tests.append(InstallTestCase)
            active_tests.append(UninstallTestCase)

        for test in active_tests:
            self.addTests(loader.loadTestsFromTestCase(test))

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
