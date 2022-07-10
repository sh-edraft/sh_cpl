import os
import shutil
import traceback
import unittest
from typing import Optional
from unittest import TestResult

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_translation.translation_test_case import TranslationTestCase


class TranslationTestSuite(unittest.TestSuite):

    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self._result: Optional[TestResult] = None
        self._is_online = True

        active_tests = [
            TranslationTestCase
        ]

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
