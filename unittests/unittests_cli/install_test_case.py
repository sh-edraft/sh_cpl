import json
import os
import shutil
import subprocess
import sys
import unittest

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class InstallTestCase(CommandTestCase):

    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = 'install-test-source'
        self._project_file = f'src/{String.convert_to_snake_case(self._source)}/{self._source}.json'

    def _get_project_settings(self):
        with open(os.path.join(os.getcwd(), self._project_file), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def _save_project_settings(self, settings: dict):
        with open(os.path.join(os.getcwd(), self._project_file), 'w', encoding='utf-8') as project_file:
            project_file.write(json.dumps(settings, indent=2))
            project_file.close()

    def setUp(self):
        if not os.path.exists(PLAYGROUND_PATH):
            os.makedirs(PLAYGROUND_PATH)
        
        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new('console', self._source, '--ab', '--s')
        os.chdir(os.path.join(os.getcwd(), self._source))

    def _get_installed_packages(self) -> dict:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        return dict([tuple(r.decode().split('==')) for r in reqs.split()])

    def test_install_package(self):
        version = '1.7.3'
        package_name = 'discord.py'
        package = f'{package_name}=={version}'
        CLICommands.install(package)
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn('ProjectSettings', settings)
        self.assertIn('Dependencies', settings['ProjectSettings'])
        self.assertIn(
            package,
            settings['ProjectSettings']['Dependencies']
        )
        packages = self._get_installed_packages()
        self.assertIn(package_name, packages)
        self.assertEqual(version, packages[package_name])

    def test_dev_install_package(self):
        version = '1.7.3'
        package_name = 'discord.py'
        package = f'{package_name}=={version}'
        CLICommands.install(package, is_dev=True)
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn('ProjectSettings', settings)
        self.assertIn('Dependencies', settings['ProjectSettings'])
        self.assertIn('DevDependencies', settings['ProjectSettings'])
        self.assertNotIn(
            package,
            settings['ProjectSettings']['Dependencies']
        )
        self.assertIn(
            package,
            settings['ProjectSettings']['DevDependencies']
        )
        packages = self._get_installed_packages()
        self.assertIn(package_name, packages)
        self.assertEqual(version, packages[package_name])

    def _test_install_all(self):
        version = '1.7.3'
        package_name = 'discord.py'
        package = f'{package_name}=={version}'
        settings = self._get_project_settings()
        self.assertIn('ProjectSettings', settings)
        self.assertIn('Dependencies', settings['ProjectSettings'])
        self.assertIn('DevDependencies', settings['ProjectSettings'])
        self.assertNotIn(
            package,
            settings['ProjectSettings']['Dependencies']
        )
        self.assertIn('DevDependencies', settings['ProjectSettings'])
        self.assertNotIn(
            package,
            settings['ProjectSettings']['Dependencies']
        )
        settings['ProjectSettings']['Dependencies'].append(package)
        settings['ProjectSettings']['DevDependencies'].append(package)
        self._save_project_settings(settings)
        CLICommands.install()
        new_settings = self._get_project_settings()
        self.assertEqual(settings, new_settings)
        self.assertIn('ProjectSettings', new_settings)
        self.assertIn('Dependencies', new_settings['ProjectSettings'])
        self.assertIn('DevDependencies', new_settings['ProjectSettings'])
        self.assertIn(
            package,
            new_settings['ProjectSettings']['Dependencies']
        )
        self.assertIn(
            package,
            new_settings['ProjectSettings']['DevDependencies']
        )
        packages = self._get_installed_packages()
        self.assertIn(package_name, packages)
        self.assertEqual(version, packages[package_name])


