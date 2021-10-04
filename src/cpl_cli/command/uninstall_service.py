import json
import os
import subprocess
import textwrap

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

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Uninstalls given package via pip
        Usage: cpl uninstall <package>
        
        Arguments:
            package     The package to uninstall
        """)

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
            with open(os.path.join(self._env.working_directory, f'{self._config.get_configuration("ProjectName")}.json'), 'w') as project_file:
                project_file.write(json.dumps(config, indent=2))
                project_file.close()

        Console.write_line(f'Removed {package}')
        Pip.reset_executable()
