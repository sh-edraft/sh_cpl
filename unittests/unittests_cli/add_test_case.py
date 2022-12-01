import json
import os

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class AddTestCase(CommandTestCase):

    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = 'add-test-project'
        self._target = 'add-test-library'
        self._project_file = f'src/{String.convert_to_snake_case(self._source)}/{self._source}.json'

    def _get_project_settings(self):
        with open(os.path.join(os.getcwd(), self._project_file), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def setUp(self):
        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))
        CLICommands.new('console', self._target, '--ab', '--s')

    def test_add(self):
        CLICommands.add(self._source, self._target)
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn('ProjectSettings', settings)
        self.assertIn('ProjectReferences', settings['BuildSettings'])
        self.assertIn('BuildSettings', settings)
        self.assertIn(
            f'../{String.convert_to_snake_case(self._target)}/{self._target}.json',
            settings['BuildSettings']['ProjectReferences']
        )
