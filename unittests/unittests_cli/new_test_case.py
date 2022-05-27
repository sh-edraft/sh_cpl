import json
import os
import shutil
import unittest

from cpl_core.utils import String

from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class NewTestCase(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.abspath(PLAYGROUND_PATH))

    def _test_project(self, project_type: str, name: str, *args):
        CLICommands.new(project_type, name, *args)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, name))
        self.assertTrue(os.path.exists(workspace_path))

        project_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, name, 'src', String.convert_to_snake_case(name)))
        self.assertTrue(os.path.exists(project_path))
        self.assertTrue(os.path.join(project_path, f'{name}.json'))
        self.assertTrue(os.path.join(project_path, f'main.py'))

        if '--ab' in args:
            self.assertTrue(os.path.isfile(os.path.join(project_path, f'application.py')))
        else:
            self.assertFalse(os.path.isfile(os.path.join(project_path, f'application.py')))

        # s depends on ab
        if '--ab' in args and '--s' in args:
            self.assertTrue(os.path.isfile(os.path.join(project_path, f'startup.py')))
        else:
            self.assertFalse(os.path.isfile(os.path.join(project_path, f'startup.py')))

        if project_type == 'unittest':
            self.assertTrue(os.path.isfile(os.path.join(project_path, f'test_case.py')))
        else:
            self.assertFalse(os.path.isfile(os.path.join(project_path, f'test_case.py')))

    def _test_sub_project(self, project_type: str, name: str, workspace_name: str, *args):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), workspace_name)))
        CLICommands.new(project_type, name, *args)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name))
        self.assertTrue(os.path.exists(workspace_path))

        project_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name, 'src', String.convert_to_snake_case(name)))
        self.assertTrue(os.path.exists(project_path))
        self.assertTrue(os.path.join(project_path, f'{name}.json'))
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), '../')))

    def _test_sub_directory_project(self, project_type: str, directory: str, name: str, workspace_name: str, *args):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), workspace_name)))
        CLICommands.new(project_type, f'{directory}/{name}', *args)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name))
        self.assertTrue(os.path.exists(workspace_path))

        project_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name, f'src/{directory}', String.convert_to_snake_case(name)))
        self.assertTrue(os.path.exists(project_path))
        project_file = os.path.join(project_path, f'{name}.json')
        self.assertTrue(project_file)
        project_json = {}
        with open(project_file, 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        project_settings = project_json['ProjectSettings']
        build_settings = project_json['BuildSettings']

        self.assertEqual(project_settings['Name'], name)
        self.assertEqual(build_settings['ProjectType'], 'library')
        self.assertEqual(build_settings['OutputPath'], '../../dist')
        self.assertEqual(build_settings['Main'], f'{String.convert_to_snake_case(name)}.main')
        self.assertEqual(build_settings['EntryPoint'], name)

        os.chdir(os.path.abspath(os.path.join(os.getcwd(), '../')))

    def test_console(self):
        self._test_project('console', 'test-console', '--ab', '--s')

    def test_console_without_s(self):
        self._test_project('console', 'test-console-without-s', '--ab')

    def test_console_without_ab(self):
        self._test_project('console', 'test-console-without-ab', '--sp')

    def test_console_without_anything(self):
        self._test_project('console', 'test-console-without-anything', '--n')

    def test_sub_console(self):
        self._test_sub_project('console', 'test-sub-console', 'test-console', '--ab', '--s', '--sp')

    def test_library(self):
        self._test_project('library', 'test-library', '--ab', '--s', '--sp')

    def test_sub_library(self):
        self._test_sub_project('library', 'test-sub-library', 'test-console', '--ab', '--s', '--sp')

    def test_sub_directory_library(self):
        self._test_sub_directory_project('library', 'directory', 'test-sub-library', 'test-console', '--ab', '--s', '--sp')

    def test_unittest(self):
        self._test_project('unittest', 'test-unittest', '--ab')

    def test_sub_unittest(self):
        self._test_sub_project('unittest', 'test-unittest', 'test-console', '--ab', '--s', '--sp')
