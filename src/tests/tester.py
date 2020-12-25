import unittest
from typing import Type

from tests.cases.service.provider_test import ProviderTest
from tests.cases.time.time_format_settings_test import TimeFormatSettingsTest
from tests.cases.utils.credential_manager_test import CredentialManagerTest


class Tester:

    def __init__(self):
        self._suite = unittest.TestSuite()
        self._cases: list[Type[unittest.TestCase]] = []

    def _build_cases(self):
        for case in self._cases:
            case_functions = [method_name for method_name in dir(case) if callable(getattr(case, method_name)) and method_name.startswith('test_')]
            for function in case_functions:
                self._suite.addTest(case(function))

    def create(self):
        self._cases.append(ProviderTest)
        self._cases.append(CredentialManagerTest)
        self._cases.append(TimeFormatSettingsTest)

    def start(self):
        self._build_cases()
        runner = unittest.TextTestRunner()
        runner.run(self._suite)


if __name__ == '__main__':
    tester = Tester()
    tester.create()
    tester.start()
