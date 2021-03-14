import json
import os
import subprocess

from cpl.application import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.utils.pip import Pip
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import ProjectSettingsNameEnum, VersionSettingsNameEnum, BuildSettingsNameEnum
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings


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

        Pip.set_executable(self._project_settings.python_path)

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
                ProjectSettings.__name__: self._get_project_settings_dict(self._project_settings),
                BuildSettings.__name__: self._get_build_settings_dict(self._build_settings)
            }
            with open(os.path.join(self._runtime.working_directory, 'cpl.json'), 'w') as project_file:
                project_file.write(json.dumps(config, indent=2))
                project_file.close()

        Console.write_line(f'Removed {package}')
        Pip.reset_executable()
