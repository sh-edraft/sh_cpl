import unittest
from typing import Optional
from unittest import TestResult

from unittests_translation.translation_test_case import TranslationTestCase


class TranslationTestSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)

        loader = unittest.TestLoader()
        self._result: Optional[TestResult] = None
        self._is_online = True

        active_tests = [TranslationTestCase]

        for test in active_tests:
            self.addTests(loader.loadTestsFromTestCase(test))

    def run(self, *args):
        self._result = super().run(*args)
