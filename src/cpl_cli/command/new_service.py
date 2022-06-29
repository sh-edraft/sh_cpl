import os
import sys
import textwrap
from typing import Optional

from packaging import version

import cpl_cli
import cpl_core
from cpl_cli.configuration.venv_helper_service import VenvHelper
from cpl_cli.source_creator.unittest_builder import UnittestBuilder

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.console.console import Console
from cpl_core.utils.string import String
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

        self._workspace: WorkspaceSettings = self._config.get_configuration(WorkspaceSettings)
        self._project: ProjectSettings = ProjectSettings()
        self._project_dict = {}
        self._build: BuildSettings = BuildSettings()
        self._build_dict = {}
        self._project_json = {}

        self._name: str = ''
        self._rel_path: str = ''
        self._schematic: ProjectTypeEnum = ProjectTypeEnum.console
        self._use_nothing: bool = False
        self._use_application_api: bool = False
        self._use_startup: bool = False
        self._use_service_providing: bool = False
        self._use_async: bool = False
        self._use_venv: bool = False

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Generates a workspace and initial project or add a project to workspace.
        Usage: cpl new <type> <name>
        
        Arguments:
            type        The project type of the initial project
            name        Name of the workspace or the project
            
        Types:
            console
            library
        """)

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
            'library (l|L) <name>',
        ]
        Console.write_line('Available Schematics:')
        for name in schematics:
            Console.write(f'\n\t{name} ')

    def _create_project_settings(self):
        self._rel_path = os.path.dirname(self._name)
        self._project_dict = {
            ProjectSettingsNameEnum.name.value: os.path.basename(self._name),
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
                f'cpl-core>={version.parse(cpl_core.__version__)}'
            ],
            ProjectSettingsNameEnum.dev_dependencies.value: [
                f'cpl-cli>={version.parse(cpl_cli.__version__)}'
            ],
            ProjectSettingsNameEnum.python_version.value: f'>={sys.version.split(" ")[0]}',
            ProjectSettingsNameEnum.python_path.value: {
                sys.platform: '../../venv/bin/python' if self._use_venv else ''
            },
            ProjectSettingsNameEnum.classifiers.value: []
        }

        self._project.from_dict(self._project_dict)

    def _create_build_settings(self):
        self._build_dict = {
            BuildSettingsNameEnum.project_type.value: self._schematic,
            BuildSettingsNameEnum.source_path.value: '',
            BuildSettingsNameEnum.output_path.value: '../../dist',
            BuildSettingsNameEnum.main.value: f'{String.convert_to_snake_case(self._project.name)}.main',
            BuildSettingsNameEnum.entry_point.value: self._project.name,
            BuildSettingsNameEnum.include_package_data.value: False,
            BuildSettingsNameEnum.included.value: [],
            BuildSettingsNameEnum.excluded.value: [
                '*/__pycache__',
                '*/logs',
                '*/tests'
            ],
            BuildSettingsNameEnum.package_data.value: {},
            BuildSettingsNameEnum.project_references.value: []
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
            project_path = os.path.join(self._env.working_directory, self._rel_path, self._project.name)
        else:
            project_path = os.path.join(self._env.working_directory, 'src', self._rel_path, String.convert_to_snake_case(self._project.name))

        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.write_line(project_path)
            Console.error('Project path is not empty\n')
            return None

        return project_path

    def _get_project_information(self, is_unittest=False):
        """
        Gets project information's from user
        :return:
        """
        if self._use_application_api or self._use_startup or self._use_service_providing or self._use_async or self._use_nothing:
            Console.set_foreground_color(ForegroundColorEnum.default)
            Console.write_line('Skipping question due to given flags')
            return

        if not is_unittest:
            self._use_application_api = Console.read('Do you want to use application base? (y/n) ').lower() == 'y'

        if not is_unittest and self._use_application_api:
            self._use_startup = Console.read('Do you want to use startup? (y/n) ').lower() == 'y'

        if not is_unittest and not self._use_application_api:
            self._use_service_providing = Console.read('Do you want to use service providing? (y/n) ').lower() == 'y'

        if not self._use_async:
            self._use_async = Console.read('Do you want to use async? (y/n) ').lower() == 'y'

        Console.set_foreground_color(ForegroundColorEnum.default)

    def _console(self, args: list[str]):
        """
        Generates new console project
        :param args:
        :return:
        """
        self._create_project_settings()
        self._create_build_settings()
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information()
        project_name = self._project.name
        if self._rel_path != '':
            project_name = f'{self._rel_path}/{project_name}'
        try:
            ConsoleBuilder.build(
                path,
                self._use_application_api,
                self._use_startup,
                self._use_service_providing,
                self._use_async,
                project_name,
                self._project_json,
                self._workspace
            )
        except Exception as e:
            Console.error('Could not create project', str(e))

    def _unittest(self, args: list[str]):
        """
        Generates new unittest project
        :param args:
        :return:
        """
        self._create_project_settings()
        self._create_build_settings()
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information(is_unittest=True)
        project_name = self._project.name
        if self._rel_path != '':
            project_name = f'{self._rel_path}/{project_name}'
        try:
            UnittestBuilder.build(
                path,
                self._use_application_api,
                self._use_async,
                project_name,
                self._project_json,
                self._workspace
            )
        except Exception as e:
            Console.error('Could not create project', str(e))

    def _library(self, args: list[str]):
        """
        Generates new library project
        :param args:
        :return:
        """
        self._create_project_settings()
        self._create_build_settings()
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information()
        project_name = self._project.name
        if self._rel_path != '':
            project_name = f'{self._rel_path}/{project_name}'
        try:
            LibraryBuilder.build(
                path,
                self._use_application_api,
                self._use_startup,
                self._use_service_providing,
                self._use_async,
                project_name,
                self._project_json,
                self._workspace
            )
        except Exception as e:
            Console.error('Could not create project', str(e))

    def _create_venv(self):

        project = self._project.name
        if self._workspace is not None:
            project = self._workspace.default_project

        if self._env.working_directory.endswith(project):
            project = ''

        VenvHelper.init_venv(
            False,
            self._env,
            self._project,
            explicit_path=os.path.join(self._env.working_directory, project, self._project.python_executable.replace('../', ''))
        )

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if 'nothing' in args:
            self._use_nothing = True
            self._use_async = False
            self._use_application_api = False
            self._use_startup = False
            self._use_service_providing = False
            if 'async' in args:
                args.remove('async')
            if 'application-base' in args:
                args.remove('application-base')
            if 'startup' in args:
                args.remove('startup')
            if 'service-providing' in args:
                args.remove('service-providing')

        if 'async' in args:
            self._use_async = True
            args.remove('async')
        if 'application-base' in args:
            self._use_application_api = True
            args.remove('application-base')
        if 'startup' in args:
            self._use_startup = True
            args.remove('startup')
        if 'service-providing' in args:
            self._use_service_providing = True
            args.remove('service-providing')
        if 'venv' in args:
            self._use_venv = True
            args.remove('venv')

        console = self._config.get_configuration(ProjectTypeEnum.console.value)
        library = self._config.get_configuration(ProjectTypeEnum.library.value)
        unittest = self._config.get_configuration(ProjectTypeEnum.unittest.value)
        if console is not None and library is None and unittest is None:
            self._name = console
            self._schematic = ProjectTypeEnum.console.value
            self._console(args)
            if self._use_venv:
                self._create_venv()

        elif console is None and library is not None and unittest is None:
            self._name = library
            self._schematic = ProjectTypeEnum.library.value
            self._library(args)
            if self._use_venv:
                self._create_venv()

        elif console is None and library is None and unittest is not None:
            self._name = unittest
            self._schematic = ProjectTypeEnum.unittest.value
            self._unittest(args)
            if self._use_venv:
                self._create_venv()

        else:
            self._help('Usage: cpl new <schematic> [options]')
            return
