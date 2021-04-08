import json
import os
import subprocess

from packaging import version

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl.utils.pip import Pip
from cpl_cli.cli_settings import CLISettings
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper
from cpl_cli.error import Error


class InstallService(CommandABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC, build_settings: BuildSettings,
                 project_settings: ProjectSettings, cli_settings: CLISettings):
        """
        Service for the CLI command install
        :param config:
        :param env:
        :param build_settings:
        :param project_settings:
        :param cli_settings:
        """
        CommandABC.__init__(self)

        self._config = config
        self._env = env
        self._build_settings = build_settings
        self._project_settings = project_settings
        self._cli_settings = cli_settings

        self._project_file = f'{self._config.get_configuration("ProjectName")}.json'

    def _install_project(self):
        """
        Installs dependencies of CPl project
        :return:
        """

        if self._project_settings is None or self._build_settings is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if self._project_settings.dependencies is None:
            Error.error(f'Found invalid dependencies in {self._project_file}.')
            return

        Pip.set_executable(self._project_settings.python_executable)
        for dependency in self._project_settings.dependencies:
            Console.spinner(
                f'Installing: {dependency}',
                Pip.install, dependency,
                source=self._cli_settings.pip_path if 'sh_cpl' in dependency else None,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )

        Pip.reset_executable()

    def _install_package(self, package: str):
        """
        Installs given package
        :param package:
        :return:
        """
        is_already_in_project = False
        Pip.set_executable(self._project_settings.python_executable)

        if self._project_settings is None or self._build_settings is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if self._project_settings.dependencies is None:
            Error.error(f'Found invalid dependencies in {self._project_file}.')
            return

        package_version = ''
        name = package
        if '==' in package:
            name = package.split('==')[0]
            package_version = package.split('==')[1]

        to_remove_list = []
        for dependency in self._project_settings.dependencies:
            dependency_version = ''

            if '==' in dependency:
                dependency_version = dependency.split('==')[1]

            if name in dependency:
                if package_version != '' and version.parse(package_version) != version.parse(dependency_version):
                    to_remove_list.append(dependency)
                    break
                else:
                    is_already_in_project = True

        for to_remove in to_remove_list:
            self._project_settings.dependencies.remove(to_remove)

        local_package = Pip.get_package(package)
        if local_package is not None and local_package in self._project_settings.dependencies:
            Error.warn(f'Package {local_package} is already installed.')
            return

        elif is_already_in_project:
            Error.warn(f'Package {package} is already installed.')
            return

        Console.spinner(
            f'Installing: {package}',
            Pip.install, package,
            source=self._cli_settings.pip_path if 'sh_cpl' in package else None,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
        new_package = Pip.get_package(name)
        if new_package is None \
                or '==' in package and \
                version.parse(package.split('==')[1]) != version.parse(new_package.split('==')[1]):
            Console.error(f'Installation of package {package} failed')
            return

        if not is_already_in_project:
            new_name = package
            if '==' in new_package:
                new_name = new_package
            elif '==' in name:
                new_name = name

            if '/' in new_name:
                new_name = new_name.split('/')[0]

            if '\r' in new_name:
                new_name = new_name.replace('\r', '')

            self._project_settings.dependencies.append(new_name)

            config = {
                ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(self._project_settings),
                BuildSettings.__name__: SettingsHelper.get_build_settings_dict(self._build_settings)
            }

            with open(os.path.join(self._env.working_directory, self._project_file), 'w') as project_file:
                project_file.write(json.dumps(config, indent=2))
                project_file.close()

        Pip.reset_executable()

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            self._install_project()
        else:
            self._install_package(args[0])
