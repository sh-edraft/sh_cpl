import os.path

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class GenerateTestCase(CommandTestCase):
    _project = 'test-console'
    _t_path = 'test'
    _skip_tear_down = True

    @classmethod
    def setUpClass(cls):
        CommandTestCase.setUpClass()
        CLICommands.new('console', cls._project, '--ab', '--s', '--venv')

    def setUp(self):
        os.chdir(PLAYGROUND_PATH)

    def _test_file(self, schematic: str, suffix: str, path=None):
        file = f'GeneratedFile{"OnReady" if schematic == "event" else ""}'
        expected_path = f'generated_file{"_on_ready" if schematic == "event" else ""}{suffix}.py'

        if path is not None:
            file = f'{path}/{file}'
            expected_path = f'{path}/{expected_path}'

        CLICommands.generate(schematic, file)
        file_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, expected_path))
        file_exists = os.path.exists(file_path)
        self.assertTrue(file_exists)

    def _test_file_with_project(self, schematic: str, suffix: str, path=None, enter=True):
        file = f'GeneratedFile{"OnReady" if schematic == "event" else ""}'
        excepted_path = f'generated_file{"_on_ready" if schematic == "event" else ""}{suffix}.py'
        if path is not None:
            excepted_path = f'{self._project}/src/{String.convert_to_snake_case(self._project)}/{path}/generated_file_in_project{"_on_ready" if schematic == "event" else ""}{suffix}.py'
            if enter:
                os.chdir(path)
                excepted_path = f'{path}/src/{String.convert_to_snake_case(self._project)}/generated_file_in_project{"_on_ready" if schematic == "event" else ""}{suffix}.py'

            file = f'{path}/GeneratedFileInProject{"OnReady" if schematic == "event" else ""}'

        CLICommands.generate(schematic, file)
        file_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, excepted_path))
        print(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_abc(self):
        self._test_file('abc', '_abc')
        self._test_file('abc', '_abc', path=self._t_path)
        self._test_file('abc', '_abc', path=f'{self._t_path}/{self._t_path}')
        self._test_file_with_project('abc', '_abc', path=self._project)
        os.chdir(f'src/{String.convert_to_snake_case(self._project)}')
        self._test_file_with_project('abc', '_abc', path='test', enter=False)

    def test_class(self):
        self._test_file('class', '')
        self._test_file('class', '', path=self._t_path)
        self._test_file_with_project('class', '', path=self._project)

    def test_enum(self):
        self._test_file('enum', '_enum')
        self._test_file('enum', '_enum', path=self._t_path)
        self._test_file_with_project('enum', '_enum', path=self._project)
        os.chdir(f'src/{String.convert_to_snake_case(self._project)}')
        self._test_file_with_project('enum', '_enum', path='test', enter=False)

    def test_pipe(self):
        self._test_file('pipe', '_pipe')
        self._test_file('pipe', '_pipe', path=self._t_path)
        self._test_file_with_project('pipe', '_pipe', path=self._project)

    def test_service(self):
        self._test_file('service', '_service')
        self._test_file_with_project('service', '_service', path=self._project)

    def test_settings(self):
        self._test_file('settings', '_settings')
        self._test_file_with_project('settings', '_settings', path=self._project)

    def test_test_case(self):
        self._test_file('test-case', '_test_case')
        self._test_file_with_project('test-case', '_test_case', path=self._project)

    def test_thread(self):
        self._test_file('thread', '_thread')
        self._test_file_with_project('thread', '_thread', path=self._project)

    def test_validator(self):
        self._test_file('validator', '_validator')
        self._test_file_with_project('validator', '_validator', path=self._project)

    def test_discord_command(self):
        self._test_file('command', '_command')
        self._test_file_with_project('command', '_command', path=self._project)

    def test_discord_event(self):
        self._test_file('event', '_event')
        self._test_file_with_project('event', '_event', path=self._project)
