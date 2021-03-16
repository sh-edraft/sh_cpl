import json
import os
import subprocess

from packaging import version

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.utils.pip import Pip
from cpl_cli.cli_settings import CLISettings
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper
from cpl_cli.error import Error


class InstallService(CommandABC):

    def __init__(self, runtime: ApplicationRuntimeABC, build_settings: BuildSettings, project_settings: ProjectSettings,
                 cli_settings: CLISettings):
        """
        Service for the CLI command install
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

    def _install_project(self):
        """
        Installs dependencies of CPl project
        :return:
        """

        if self._project_settings is None or self._build_settings is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if self._project_settings.dependencies is None:
            Error.error('Found invalid dependencies in cpl.json.')
            return

        Pip.set_executable(self._project_settings.python_path)
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
        Pip.set_executable(self._project_settings.python_path)

        if self._project_settings is None or self._build_settings is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if self._project_settings.dependencies is None:
            Error.error('Found invalid dependencies in cpl.json.')
            return

        package_version = ''
        name = ''
        if '==' in package:
            name = package.split('==')[0]
            package_version = package.split('==')[1]

        to_remove_list = []
        for dependency in self._project_settings.dependencies:
            dependency_version = ''

            if '==' in dependency:
                dependency_version = dependency.split('==')[1]

            if version.parse(package_version) != version.parse(dependency_version):
                to_remove_list.append(dependency)
                break

            if package in dependency:
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
        if new_package is None:
            Console.error(f'Installation of package {package} failed')
            return

        if not is_already_in_project:
            new_package = Pip.get_package(package)
            if new_package is not None:
                new_package = package

            if '/' in new_package:
                new_package = new_package.split('/')[0]

            if '\\' in new_package:
                new_package = new_package.split('\\')[0]

            self._project_settings.dependencies.append(new_package)

            config = {
                ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(self._project_settings),
                BuildSettings.__name__: SettingsHelper.get_build_settings_dict(self._build_settings)
            }
            with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project_file:
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

        Console.write('\n')
