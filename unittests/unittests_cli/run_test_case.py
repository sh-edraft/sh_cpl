import json
import os
import shutil
import unittest

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class RunTestCase(CommandTestCase):

    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = 'run-test'
        self._project_file = f'src/{String.convert_to_snake_case(self._source)}/{self._source}.json'
        self._appsettings = f'src/{String.convert_to_snake_case(self._source)}/appsettings.json'
        self._application = f'src/{String.convert_to_snake_case(self._source)}/application.py'
        self._test_code = f"""
        import json
        settings = dict()
        with open('appsettings.json', 'r', encoding='utf-8') as cfg:
            # load json
            settings = json.load(cfg)
            cfg.close()
            
        settings['RunTest']['WasStarted'] = 'True'
        
        with open('appsettings.json', 'w', encoding='utf-8') as project_file:
            project_file.write(json.dumps(settings, indent=2))
            project_file.close()
        """

    def _get_appsettings(self):
        with open(os.path.join(os.getcwd(), self._appsettings), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def _save_appsettings(self, settings: dict):
        with open(os.path.join(os.getcwd(), self._appsettings), 'w', encoding='utf-8') as project_file:
            project_file.write(json.dumps(settings, indent=2))
            project_file.close()

    def setUp(self):
        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))
        settings = {'RunTest': {'WasStarted': 'False'}}
        self._save_appsettings(settings)
        with open(os.path.join(os.getcwd(), self._application), 'a', encoding='utf-8') as file:
            file.write(f'\t\t{self._test_code}')
            file.close()

    def test_run(self):
        CLICommands.run(is_dev=True, output=True)
        settings = self._get_appsettings()
        self.assertNotEqual(settings, {})
        self.assertIn('RunTest', settings)
        self.assertIn('WasStarted', settings['RunTest'])
        self.assertEqual(
            'True',
            settings['RunTest']['WasStarted']
        )

    def test_run_by_project(self):
        os.chdir(os.path.join(os.getcwd()))
        CLICommands.run(self._source, is_dev=True)
        settings = self._get_appsettings()
        self.assertNotEqual(settings, {})
        self.assertIn('RunTest', settings)
        self.assertIn('WasStarted', settings['RunTest'])
        self.assertEqual(
            'True',
            settings['RunTest']['WasStarted']
        )
