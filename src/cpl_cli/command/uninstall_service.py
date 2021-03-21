import json
import os
import subprocess

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.utils.pip import Pip
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper


class UninstallService(CommandABC):

    def __init__(self, runtime: ApplicationRuntimeABC, build_settings: BuildSettings,
                 project_settings: ProjectSettings):
        """
        Service for the CLI command uninstall
        :param runtime:
        :param build_settings:
        :param project_settings:
        """
        CommandABC.__init__(self)

        self._runtime = runtime

        self._build_settings = build_settings
        self._project_settings = project_settings

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            Console.error(f'Expected package')
            Console.error(f'Usage: cpl uninstall <package>')
            return

        Pip.set_executable(self._project_settings.python_executable)

        package = args[0]
        is_in_dependencies = False

        pip_package = Pip.get_package(package)

        for dependency in self._project_settings.dependencies:
            if package in dependency:
                is_in_dependencies = True
                package = dependency

        if not is_in_dependencies and pip_package is None:
            Console.error(f'Package {package} not found')
            return

        elif not is_in_dependencies and pip_package is not None:
            package = pip_package

        Console.spinner(
            f'Uninstalling: {package}',
            Pip.uninstall, package,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        if package in self._project_settings.dependencies:
            self._project_settings.dependencies.remove(package)
            config = {
                ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(self._project_settings),
                BuildSettings.__name__: SettingsHelper.get_build_settings_dict(self._build_settings)
            }
            with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project_file:
                project_file.write(json.dumps(config, indent=2))
                project_file.close()

        Console.write_line(f'Removed {package}')
        Pip.reset_executable()
