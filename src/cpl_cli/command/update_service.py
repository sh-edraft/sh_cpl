import json
import os
import subprocess
import sys

from cpl.application import ApplicationRuntimeABC
from cpl.console import ForegroundColorEnum
from cpl.console.console import Console
from cpl.utils.pip import Pip
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.project_settings import ProjectSettings


class UpdateService(CommandABC):

    def __init__(self, runtime: ApplicationRuntimeABC, project_settings: ProjectSettings):
        CommandABC.__init__(self)

        self._runtime = runtime
        self._project_settings = project_settings

    @staticmethod
    def _install_package(name: str):
        if 'sh_cpl' in name:
            Pip.install(
                name,
                '--upgrade',
                '--upgrade-strategy',
                'eager',
                source='https://pip.sh-edraft.de',
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            Pip.install(
                name,
                '--upgrade',
                '--upgrade-strategy',
                'eager',
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def _update_project_dependencies(self):
        for package in self._project_settings.dependencies:
            name = package
            if '==' in package:
                name = package.split('==')[0]

            self._install_package(name)

            new_package = Pip.get_package(name)
            if new_package is None:
                Console.error(f'Update for package {package} failed')
                return

            self._project_json_update_dependency(package, new_package)

    def _check_project_dependencies(self):
        Console.spinner(
            'Collecting installed dependencies', self._update_project_dependencies,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
        Console.write_line(f'Found {len(self._project_settings.dependencies)} dependencies.')

    @staticmethod
    def _check_outdated():
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
        content = ''
        with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'r') as project:
            content = project.read()
            project.close()

        if content == '' or content == '{}':
            return

        if old_package in content:
            content = content.replace(old_package, new_package)

        with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project:
            project.write(json.dumps(json.loads(content), indent=2))
            project.close()

    def run(self, args: list[str]):
        Pip.set_executable(self._project_settings.python_path)
        self._check_project_dependencies()
        self._check_outdated()
        Pip.reset_executable()

        Console.write('\n')
