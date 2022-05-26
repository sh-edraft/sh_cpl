import os.path
import unittest

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class GenerateTestCase(unittest.TestCase):

    def _test_file(self, schematic: str, suffix: str):
        CLICommands.generate(schematic, 'GeneratedFile')
        file_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, f'generated_file{suffix}.py'))
        file_exists = os.path.exists(file_path)
        self.assertTrue(file_exists)
        os.remove(file_path)

    def test_abc(self):
        self._test_file('abc', '_abc')

    def test_class(self):
        self._test_file('class', '')

    def test_enum(self):
        self._test_file('enum', '_enum')

    def test_pipe(self):
        self._test_file('pipe', '_pipe')

    def test_service(self):
        self._test_file('service', '_service')

    def test_settings(self):
        self._test_file('settings', '_settings')

    def test_test_case(self):
        self._test_file('test_case', '_test_case')

    def test_thread(self):
        self._test_file('thread', '_thread')

    def test_validator(self):
        self._test_file('validator', '_validator')
