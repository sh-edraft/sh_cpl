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
    def _get_outdated() -> bytes:
        return subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated"])

    def _update_project_dependencies(self):
        for package in self._project_settings.dependencies:
            name = package
            if '==' in package:
                name = package.split('==')[0]

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

            self._project_json_update_dependency(package, Pip.get_package(name))

    def _check_project_dependencies(self):
        Console.spinner(
            'Collecting installed dependencies', self._update_project_dependencies,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
        Console.write_line(f'Found {len(self._project_settings.dependencies)} dependencies.')

    def _check_outdated(self):
        table_str: bytes = Console.spinner(
            'Analyzing for available package updates', self._get_outdated,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        Console.write_line('\tAvailable updates for packages:')
        table = str(table_str, 'utf-8').split('\n')
        for row in table:
            Console.write_line(f'\t{row}')

        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(f'\tUpdate with {sys.executable} -m pip install --upgrade <package>')
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
        # target update discord 1.5.1 to discord 1.6.0
        self._check_project_dependencies()
        self._check_outdated()

        Console.write('\n')
