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


class UninstallTestCase(CommandTestCase):

    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = 'uninstall-test-source'
        self._project_file = f'src/{String.convert_to_snake_case(self._source)}/{self._source}.json'
        self._version = '1.7.3'
        self._package_name = 'discord.py'
        self._package = f'{self._package_name}=={self._version}'

    def _get_project_settings(self):
        with open(os.path.join(os.getcwd(), self._project_file), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

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

    def test_uninstall(self):
        CLICommands.install(self._package)
        CLICommands.uninstall(self._package)
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn('ProjectSettings', settings)
        self.assertIn('Dependencies', settings['ProjectSettings'])
        self.assertNotIn(
            self._package,
            settings['ProjectSettings']['Dependencies']
        )
        self.assertNotIn(
            self._package,
            settings['ProjectSettings']['DevDependencies']
        )
        packages = self._get_installed_packages()
        self.assertNotIn(self._package_name, packages)

    def test_dev_uninstall(self):
        CLICommands.install(self._package, is_dev=True)
        CLICommands.uninstall(self._package, is_dev=True)
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn('ProjectSettings', settings)
        self.assertIn('Dependencies', settings['ProjectSettings'])
        self.assertIn('DevDependencies', settings['ProjectSettings'])
        self.assertNotIn(
            self._package,
            settings['ProjectSettings']['Dependencies']
        )
        self.assertNotIn(
            self._package,
            settings['ProjectSettings']['DevDependencies']
        )
        packages = self._get_installed_packages()
        self.assertNotIn(self._package_name, packages)
