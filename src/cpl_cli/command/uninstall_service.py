import json
import os
import subprocess
import textwrap
import time

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.utils.pip import Pip
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper


class UninstallService(CommandABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC, build_settings: BuildSettings,
                 project_settings: ProjectSettings):
        """
        Service for the CLI command uninstall
        :param config:
        :param env:
        :param build_settings:
        :param project_settings:
        """
        CommandABC.__init__(self)

        self._config = config
        self._env = env
        self._build_settings = build_settings
        self._project_settings = project_settings
        
        self._is_simulating = False
        self._is_virtual = False
        self._project_file = f'{self._project_settings.name}.json'

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Uninstalls given package via pip
        Usage: cpl uninstall <package>
        
        Arguments:
            package     The package to uninstall
        """)
        
    def _wait(self, t: int, *args, source: str = None, stdout=None, stderr=None):
        time.sleep(t)

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            Console.error(f'Expected package')
            Console.error(f'Usage: cpl uninstall <package>')
            return

        if '--virtual' in args:
            self._is_virtual = True
            args.remove('--virtual')
            Console.write_line('Running in virtual mode:')
        
        if '--simulate' in args:
            self._is_virtual = True
            args.remove('--simulate')
            Console.write_line('Running in simulation mode:')

        if not self._is_virtual:
            Pip.set_executable(self._project_settings.python_executable)

        package = args[0]
        is_in_dependencies = False

        if not self._is_virtual:
            pip_package = Pip.get_package(package)
        else:
            pip_package = package

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
            Pip.uninstall if not self._is_virtual else self._wait, package if not self._is_virtual else 2,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        if package in self._project_settings.dependencies:
            self._project_settings.dependencies.remove(package)
            if not self._is_simulating:
                config = {
                    ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(self._project_settings),
                    BuildSettings.__name__: SettingsHelper.get_build_settings_dict(self._build_settings)
                }
                with open(os.path.join(self._env.working_directory, self._project_file), 'w') as project_file:
                    project_file.write(json.dumps(config, indent=2))
                    project_file.close()

        Console.write_line(f'Removed {package}')
        if not self._is_virtual:
            Pip.reset_executable()
