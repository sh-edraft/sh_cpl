import os
import shutil
import unittest

from cpl_core.utils import String

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class NewTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def _test_project(self, project_type: str, name: str, *args):
        CLICommands.new(project_type, name, *args)
        project_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, String.convert_to_snake_case(name)))
        self.assertTrue(os.path.exists(project_path))
        shutil.rmtree(project_path)

    def test_console(self):
        print(f'{__name__} new console')
        self._test_project('console', 'test-console', '--ab', '--s', '--sp')

    def test_library(self):
        print(f'{__name__} new library')
        self._test_project('library', 'test-library', '--ab', '--s', '--sp')

    def test_unittest(self):
        print(f'{__name__} new unittests')
        self._test_project('unittest', 'test-unittest', '--ab', '--s', '--sp')
