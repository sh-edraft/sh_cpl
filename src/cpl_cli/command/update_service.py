import json
import os
import subprocess

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.utils.pip import Pip
from cpl_cli.cli_settings import CLISettings
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper


class UpdateService(CommandABC):

    def __init__(self,
                 runtime: ApplicationRuntimeABC,
                 build_settings: BuildSettings,
                 project_settings: ProjectSettings,
                 cli_settings: CLISettings):
        """
        Service for the CLI command update
        :param runtime:
        :param build_settings:
        :param project_settings:
        :param cli_settings:
        """
        CommandABC.__init__(self)

        self._runtime = runtime
        self._build_settings = build_settings
        self._project_settings = project_settings
        self._cli_settings = cli_settings

    def _update_project_dependencies(self):
        """
        Updates project dependencies
        :return:
        """
        for package in self._project_settings.dependencies:
            name = package
            if '==' in package:
                name = package.split('==')[0]

            Pip.install(
                name,
                '--upgrade',
                '--upgrade-strategy',
                'eager',
                source=self._cli_settings.pip_path if 'sh_cpl' in name else None,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            new_package = Pip.get_package(name)
            if new_package is None:
                Console.error(f'Update for package {package} failed')
                return

            self._project_json_update_dependency(package, new_package)

    def _check_project_dependencies(self):
        """
        Checks project dependencies for updates
        :return:
        """
        Console.spinner(
            'Collecting installed dependencies', self._update_project_dependencies,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
        Console.write_line(f'Found {len(self._project_settings.dependencies)} dependencies.')

    @staticmethod
    def _check_outdated():
        """
        Checks for outdated packages in project
        :return:
        """
        table_str: bytes = Console.spinner(
            'Analyzing for available package updates', Pip.get_outdated,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        table = str(table_str, 'utf-8').split('\n')
        if len(table) > 1 and table[0] != '':
            Console.write_line('\tAvailable updates for packages:')
            for row in table:
                Console.write_line(f'\t{row}')

            Console.set_foreground_color(ForegroundColorEnum.yellow)
            Console.write_line(f'\tUpdate with {Pip.get_executable()} -m pip install --upgrade <package>')
            Console.set_foreground_color(ForegroundColorEnum.default)

    def _project_json_update_dependency(self, old_package: str, new_package: str):
        """
        Writes new package version to cpl.json
        :param old_package:
        :param new_package:
        :return:
        """
        if old_package in self._project_settings.dependencies:
            index = self._project_settings.dependencies.index(old_package)
            if '/' in new_package:
                new_package = new_package.split('/')[0]

            if '\r' in new_package:
                new_package = new_package.replace('\r', '')

            self._project_settings.dependencies[index] = new_package

        config = {
            ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(self._project_settings),
            BuildSettings.__name__: SettingsHelper.get_build_settings_dict(self._build_settings)
        }

        with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project:
            project.write(json.dumps(config, indent=2))
            project.close()

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        Pip.set_executable(self._project_settings.python_executable)
        self._check_project_dependencies()
        self._check_outdated()
        Pip.reset_executable()
