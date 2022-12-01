import json
import os
import shutil
import subprocess
import sys
import unittest

import pkg_resources

from cpl_core.utils import String

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class RunTestCase(unittest.TestCase):

    def __init__(self, methodName: str):
        unittest.TestCase.__init__(self, methodName)
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
        if not os.path.exists(PLAYGROUND_PATH):
            os.makedirs(PLAYGROUND_PATH)
        
        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))
        settings = {'RunTest': {'WasStarted': 'False'}}
        self._save_appsettings(settings)
        with open(os.path.join(os.getcwd(), self._application), 'a', encoding='utf-8') as file:
            file.write(f'\t\t{self._test_code}')
            file.close()

    def cleanUp(self):
        # remove projects
        if not os.path.exists(os.path.abspath(os.path.join(PLAYGROUND_PATH, self._source))):
            return

        shutil.rmtree(os.path.abspath(os.path.join(PLAYGROUND_PATH, self._source)))

    def test_run(self):
        CLICommands.run()
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
        CLICommands.run(self._source)
        settings = self._get_appsettings()
        self.assertNotEqual(settings, {})
        self.assertIn('RunTest', settings)
        self.assertIn('WasStarted', settings['RunTest'])
        self.assertEqual(
            'True',
            settings['RunTest']['WasStarted']
        )
