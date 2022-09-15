import pkgutil
import platform
import sys
import textwrap
import unittest

import pkg_resources
from art import text2art
from tabulate import tabulate

import cpl_cli
from cpl_core.console import ForegroundColorEnum
from termcolor import colored

from unittests_shared.cli_commands import CLICommands


class VersionTestCase(unittest.TestCase):

    def __init__(self, methodName: str):
        unittest.TestCase.__init__(self, methodName)
        self._block_banner = ""
        self._block_version = ""
        self._block_package_header = ""
        self._block_cpl_packages = ""
        self._block_packages = ""
        self._name = "CPL CLI"

    def setUp(self):
        pass

    def _get_version_output(self, version: str):
        index = 0

        for line in version.split('\n'):
            if line == "":
                continue

            if index <= 5:
                self._block_banner += f'{line}\n'

            if 7 <= index <= 9:
                self._block_version += f'{line}\n'

            if 10 <= index <= 16:
                self._block_cpl_packages += f'{line}\n'

            if index >= 18:
                self._block_packages += f'{line}\n'

            index += 1

    def test_version(self):
        packages = []
        cpl_packages = []
        dependencies = dict(tuple(str(ws).split()) for ws in pkg_resources.working_set)
        for p in dependencies:
            if str(p).startswith('cpl-'):
                cpl_packages.append([p, dependencies[p]])
                continue

            packages.append([p, dependencies[p]])

        version = CLICommands.version()
        self._get_version_output(version)
        reference_banner = colored(text2art(self._name), ForegroundColorEnum.yellow.value).split('\n')
        reference_banner = "\n".join(reference_banner[:len(reference_banner) - 1]) + '\n'
        self.assertEqual(reference_banner, self._block_banner)

        reference_version = [
            colored(f'{colored("Common Python library CLI: ")}{colored(cpl_cli.__version__)}'),
            colored(f'{colored("Python: ")}{colored(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")}'),
            colored(f'OS: {colored(f"{platform.system()} {platform.processor()}")}') + '\n'
        ]
        self.assertEqual('\n'.join(reference_version), self._block_version)
        reference_cpl_packages = [
            colored(colored(f'CPL packages:')),
            colored(f'{tabulate(cpl_packages, headers=["Name", "Version"])}') + '\n'
        ]
        self.assertEqual('\n'.join(reference_cpl_packages), self._block_cpl_packages)
        reference_packages = [
            colored(colored(f'Python packages:')),
            colored(f'{tabulate(packages, headers=["Name", "Version"])}'),
            '\x1b[0m\x1b[0m\n\x1b[0m\x1b[0m\n' # fix colored codes
        ]
        self.assertEqual('\n'.join(reference_packages), self._block_packages)
