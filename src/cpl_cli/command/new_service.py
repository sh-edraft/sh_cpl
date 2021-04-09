import json
import os
import sys
from typing import Optional

from packaging import version

import cpl

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl.utils.string import String
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name_enum import ProjectSettingsNameEnum
from cpl_cli.configuration.project_type_enum import ProjectTypeEnum
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.source_creator.console_builder import ConsoleBuilder
from cpl_cli.source_creator.library_builder import LibraryBuilder


class NewService(CommandABC):

    def __init__(self, configuration: ConfigurationABC):
        """
        Service for the CLI command new
        :param configuration:
        """
        CommandABC.__init__(self)

        self._config = configuration
        self._env = self._config.environment

        self._workspace = self._config.get_configuration(WorkspaceSettings)
        self._project: ProjectSettings = ProjectSettings()
        self._project_dict = {}
        self._build: BuildSettings = BuildSettings()
        self._build_dict = {}
        self._project_json = {}

        self._command: str = ''
        self._use_application_api: bool = False
        self._use_startup: bool = False
        self._use_service_providing: bool = False

    @staticmethod
    def _help(message: str):
        """
        Internal help output
        :param message:
        :return:
        """
        Console.error(message)

        schematics = [
            'console (c|C) <name>',
        ]
        Console.write_line('Available Schematics:')
        for name in schematics:
            Console.write(f'\n\t{name} ')

    def _create_project_settings(self, name: str):
        self._project_dict = {
            ProjectSettingsNameEnum.name.value: name,
            ProjectSettingsNameEnum.version.value: {
                VersionSettingsNameEnum.major.value: '0',
                VersionSettingsNameEnum.minor.value: '0',
                VersionSettingsNameEnum.micro.value: '0'
            },
            ProjectSettingsNameEnum.author.value: '',
            ProjectSettingsNameEnum.author_email.value: '',
            ProjectSettingsNameEnum.description.value: '',
            ProjectSettingsNameEnum.long_description.value: '',
            ProjectSettingsNameEnum.url.value: '',
            ProjectSettingsNameEnum.copyright_date.value: '',
            ProjectSettingsNameEnum.copyright_name.value: '',
            ProjectSettingsNameEnum.license_name.value: '',
            ProjectSettingsNameEnum.license_description.value: '',
            ProjectSettingsNameEnum.dependencies.value: [
                f'sh_cpl=={version.parse(cpl.__version__)}'
            ],
            ProjectSettingsNameEnum.python_version.value: f'>={sys.version.split(" ")[0]}',
            ProjectSettingsNameEnum.python_path.value: {
                sys.platform: ''
            },
            ProjectSettingsNameEnum.classifiers.value: []
        }

        self._project.from_dict(self._project_dict)

    def _create_build_settings(self):
        main = f'{String.convert_to_snake_case(self._project.name)}.main'
        if self._command == ProjectTypeEnum.library.value:
            main = f'{String.convert_to_snake_case(self._project.name)}.main'

        self._build_dict = {
            BuildSettingsNameEnum.project_type.value: self._command,
            BuildSettingsNameEnum.source_path.value: '',
            BuildSettingsNameEnum.output_path.value: '../../dist',
            BuildSettingsNameEnum.main.value: main,
            BuildSettingsNameEnum.entry_point.value: self._project.name,
            BuildSettingsNameEnum.include_package_data.value: False,
            BuildSettingsNameEnum.included.value: [],
            BuildSettingsNameEnum.excluded.value: [
                '*/__pycache__',
                '*/logs',
                '*/tests'
            ],
            BuildSettingsNameEnum.package_data.value: {}
        }
        self._build.from_dict(self._build_dict)

    def _create_project_json(self):
        """
        Creates cpl.json content
        :return:
        """
        self._project_json = {
            ProjectSettings.__name__: self._project_dict,
            BuildSettings.__name__: self._build_dict
        }

    def _get_project_path(self) -> Optional[str]:
        """
        Gets project path
        :return:
        """
        if self._workspace is None:
            project_path = os.path.join(self._env.working_directory, self._project.name)
        else:
            project_path = os.path.join(self._env.working_directory, 'src', self._project.name)

        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.error('Project path is not empty\n')
            return None

        return project_path

    def _get_project_information(self):
        """
        Gets project information's from user
        :return:
        """
        result = Console.read('Do you want to use application base? (y/n) ')
        if result.lower() == 'y':
            self._use_application_api = True

            result = Console.read('Do you want to use startup? (y/n) ')
            if result.lower() == 'y':
                self._use_startup = True
        else:
            result = Console.read('Do you want to use service providing? (y/n) ')
            if result.lower() == 'y':
                self._use_service_providing = True

        Console.set_foreground_color(ForegroundColorEnum.default)

    def _console(self, args: list[str]):
        """
        Generates new console project
        :param args:
        :return:
        """
        name = self._config.get_configuration(self._command)

        self._create_project_settings(name)
        self._create_build_settings()
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information()
        try:
            ConsoleBuilder.build(
                path,
                self._use_application_api,
                self._use_startup,
                self._use_service_providing,
                self._project.name,
                self._project_json
            )
        except Exception as e:
            Console.error('Could not create project', str(e))

    def _library(self, args: list[str]):
        """
        Generates new library project
        :param args:
        :return:
        """
        name = self._config.get_configuration(self._command)

        self._create_project_settings(name)
        self._create_build_settings()
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information()
        try:
            LibraryBuilder.build(
                path,
                self._use_application_api,
                self._use_startup,
                self._use_service_providing,
                self._project.name,
                self._project_json,
                self._workspace
            )
        except Exception as e:
            Console.error('Could not create project', str(e))

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            self._help('Usage: cpl new <schematic> [options]')
            return

        Console.write_line(1, self._workspace)

        self._command = str(args[0]).lower()
        if self._command == ProjectTypeEnum.console.value:
            self._console(args)

        elif self._command == ProjectTypeEnum.library.value:
            self._library(args)

        else:
            self._help('Usage: cpl new <schematic> [options]')
            return
