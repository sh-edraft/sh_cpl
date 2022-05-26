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
        print(f'{__name__} generate abc')
        self._test_file('abc', '_abc')

    def test_class(self):
        print(f'{__name__} generate class')
        self._test_file('class', '')

    def test_enum(self):
        print(f'{__name__} generate enum')
        self._test_file('enum', '_enum')

    def test_pipe(self):
        print(f'{__name__} generate pipe')
        self._test_file('pipe', '_pipe')

    def test_service(self):
        print(f'{__name__} generate service')
        self._test_file('service', '_service')

    def test_settings(self):
        print(f'{__name__} generate settings')
        self._test_file('settings', '_settings')

    def test_test_case(self):
        print(f'{__name__} generate test_case')
        self._test_file('test_case', '_test_case')

    def test_thread(self):
        print(f'{__name__} generate thread')
        self._test_file('thread', '_thread')

    def test_validator(self):
        print(f'{__name__} generate validator')
        self._test_file('validator', '_validator')
