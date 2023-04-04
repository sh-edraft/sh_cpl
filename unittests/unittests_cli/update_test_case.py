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


class UpdateTestCase(CommandTestCase):
    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)
        self._source = "install-test-source"
        self._project_file = f"src/{String.convert_to_snake_case(self._source)}/{self._source}.json"

        self._old_version = "1.7.1"
        self._old_package_name = "discord.py"
        self._old_package = f"{self._old_package_name}=={self._old_version}"

        # todo: better way to do shit required
        self._new_version = "2.2.2"
        self._new_package_name = "discord.py"
        self._new_package = f"{self._new_package_name}=={self._new_version}"

    def setUp(self):
        CLICommands.uninstall(self._old_package)
        CLICommands.uninstall(self._new_package)
        os.chdir(PLAYGROUND_PATH)
        # create projects
        CLICommands.new("console", self._source, "--ab", "--s")
        os.chdir(os.path.join(os.getcwd(), self._source))
        CLICommands.install(self._old_package)

    def _get_project_settings(self):
        with open(os.path.join(os.getcwd(), self._project_file), "r", encoding="utf-8") as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def _save_project_settings(self, settings: dict):
        with open(os.path.join(os.getcwd(), self._project_file), "w", encoding="utf-8") as project_file:
            project_file.write(json.dumps(settings, indent=2))
            project_file.close()

    def _get_installed_packages(self) -> dict:
        reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        return dict([tuple(r.decode().split("==")) for r in reqs.split()])

    def test_install_package(self):
        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn("ProjectSettings", settings)
        self.assertIn("Dependencies", settings["ProjectSettings"])
        self.assertIn(self._old_package, settings["ProjectSettings"]["Dependencies"])
        packages = self._get_installed_packages()
        self.assertIn(self._old_package_name, packages)
        self.assertEqual(self._old_version, packages[self._old_package_name])

        CLICommands.update()

        settings = self._get_project_settings()
        self.assertNotEqual(settings, {})
        self.assertIn("ProjectSettings", settings)
        self.assertIn("Dependencies", settings["ProjectSettings"])
        self.assertIn(self._new_package, settings["ProjectSettings"]["Dependencies"])
        packages = self._get_installed_packages()
        self.assertIn(self._new_package_name, packages)
        self.assertEqual(self._new_version, packages[self._new_package_name])
