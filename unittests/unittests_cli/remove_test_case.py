import json
import os
import unittest

from cpl_core.utils import String
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class RemoveTestCase(unittest.TestCase):

    def __init__(self, methodName: str):
        unittest.TestCase.__init__(self, methodName)
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
        os.chdir(os.path.abspath(PLAYGROUND_PATH))
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))
        CLICommands.new('console', self._target, '--ab', '--s')
        CLICommands.add(self._source, self._target)

    def test_remove(self):
        CLICommands.remove(self._target)
        path = os.path.abspath(os.path.join(os.getcwd(), f'../{String.convert_to_snake_case(self._target)}'))
        self.assertTrue(os.path.exists(os.getcwd()))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), self._project_file)))
        self.assertFalse(os.path.exists(path))
        settings = self._get_project_settings()
        self.assertIn('ProjectSettings', settings)
        self.assertIn('ProjectReferences', settings['BuildSettings'])
        self.assertIn('BuildSettings', settings)
        self.assertNotIn(
            f'../{String.convert_to_snake_case(self._target)}/{self._target}.json',
            settings['BuildSettings']['ProjectReferences']
        )
