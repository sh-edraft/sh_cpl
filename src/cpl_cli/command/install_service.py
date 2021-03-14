import json
import os
import subprocess
import sys
from typing import Optional

from cpl.application import ApplicationRuntimeABC
from cpl.configuration import ConfigurationABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.utils.pip import Pip
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import ProjectSettingsNameEnum, VersionSettingsNameEnum, BuildSettingsNameEnum
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.error import Error


class InstallService(CommandABC):

    def __init__(self, runtime: ApplicationRuntimeABC, configuration: ConfigurationABC):
        CommandABC.__init__(self)

        self._runtime = runtime
        self._config = configuration

    def _install_project(self):
        project: ProjectSettings = self._config.get_configuration(ProjectSettings)
        build: BuildSettings = self._config.get_configuration(BuildSettings)

        if project is None or build is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if project.dependencies is None:
            Error.error('Found invalid dependencies in cpl.json.')
            return

        for dependency in project.dependencies:
            Console.spinner(
                f'Installing: {dependency}',
                Pip.install, dependency,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )

    @staticmethod
    def _get_project_settings_dict(project: ProjectSettings) -> dict:
        return {
            ProjectSettingsNameEnum.name.value: project.name,
            ProjectSettingsNameEnum.version.value: {
                VersionSettingsNameEnum.major.value: project.version.major,
                VersionSettingsNameEnum.minor.value: project.version.minor,
                VersionSettingsNameEnum.micro.value: project.version.micro
            },
            ProjectSettingsNameEnum.author.value: project.author,
            ProjectSettingsNameEnum.author_email.value: project.author_email,
            ProjectSettingsNameEnum.description.value: project.description,
            ProjectSettingsNameEnum.long_description.value: project.long_description,
            ProjectSettingsNameEnum.url.value: project.url,
            ProjectSettingsNameEnum.copyright_date.value: project.copyright_date,
            ProjectSettingsNameEnum.copyright_name.value: project.copyright_name,
            ProjectSettingsNameEnum.license_name.value: project.license_name,
            ProjectSettingsNameEnum.license_description.value: project.license_description,
            ProjectSettingsNameEnum.dependencies.value: project.dependencies,
            ProjectSettingsNameEnum.python_version.value: project.python_version
        }

    @staticmethod
    def _get_build_settings_dict(build: BuildSettings) -> dict:
        return {
            BuildSettingsNameEnum.source_path.value: build.source_path,
            BuildSettingsNameEnum.output_path.value: build.output_path,
            BuildSettingsNameEnum.main.value: build.main,
            BuildSettingsNameEnum.entry_point.value: build.entry_point,
            BuildSettingsNameEnum.include_package_data.value: build.include_package_data,
            BuildSettingsNameEnum.included.value: build.included,
            BuildSettingsNameEnum.excluded.value: build.excluded,
            BuildSettingsNameEnum.package_data.value: build.package_data
        }

    def _install_package(self, package: str):
        is_already_in_project = False
        project: ProjectSettings = self._config.get_configuration(ProjectSettings)
        build: BuildSettings = self._config.get_configuration(BuildSettings)

        if project is None or build is None:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
            return

        if project.dependencies is None:
            Error.error('Found invalid dependencies in cpl.json.')
            return

        old_package = Pip.get_package(package)

        for dependency in project.dependencies:
            if package in dependency:
                is_already_in_project = True

        if old_package is not None and old_package in project.dependencies or is_already_in_project:
            Error.warn(f'Package {old_package} is already installed.')
            return

        Console.spinner(
            f'Installing: {package}',
            Pip.install, package,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        if not is_already_in_project:
            new_package = Pip.get_package(package)
            if new_package is None:
                new_package = package

            project.dependencies.append(new_package)

            config = {
                ProjectSettings.__name__: self._get_project_settings_dict(project),
                BuildSettings.__name__: self._get_build_settings_dict(build)
            }
            with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project_file:
                project_file.write(json.dumps(config, indent=2))
                project_file.close()

    def run(self, args: list[str]):
        if len(args) == 0:
            self._install_project()
        else:
            self._install_package(args[0])

        Console.write('\n')
