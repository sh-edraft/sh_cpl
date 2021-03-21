import json
import os
import sys
from typing import Optional

from packaging import version

import cpl

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name_enum import ProjectSettingsNameEnum
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum
from cpl_cli.templates.new.console.license import LicenseTemplate
from cpl_cli.templates.new.console.readme_py import ReadmeTemplate
from cpl_cli.templates.new.console.src.application import ApplicationTemplate
from cpl_cli.templates.new.console.src.main import MainWithApplicationHostAndStartupTemplate, MainWithoutApplicationHostTemplate, MainWithApplicationHostTemplate
from cpl_cli.templates.new.console.src.startup import StartupTemplate
from cpl_cli.templates.new.console.src.tests.init import TestsInitTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class NewService(CommandABC):

    def __init__(self, configuration: ConfigurationABC, runtime: ApplicationRuntimeABC):
        """
        Service for the CLI command new
        :param configuration:
        :param runtime:
        """
        CommandABC.__init__(self)

        self._config = configuration
        self._runtime = runtime

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
        self._build_dict = {
            BuildSettingsNameEnum.source_path.value: 'src',
            BuildSettingsNameEnum.output_path.value: 'dist',
            BuildSettingsNameEnum.main.value: 'main',
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
        project_path = os.path.join(self._runtime.working_directory, self._project.name)
        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.error('Project path is not empty\n')
            return None

        return project_path

    def _get_project_informations(self):
        """
        Gets project informations from user
        :return:
        """
        result = Console.read('Do you want to use application host? (y/n) ')
        if result.lower() == 'y':
            self._use_application_api = True

        if self._use_application_api:
            result = Console.read('Do you want to use startup? (y/n) ')
            if result.lower() == 'y':
                self._use_startup = True

        Console.set_foreground_color(ForegroundColorEnum.default)

        # else:
        #     result = Console.read('Do you want to use service providing? (y/n) ')
        #     if result.lower() == 'y':
        #         self._use_service_providing = True

    def _build_project_dir(self, project_path: str):
        """
        Builds the project files
        :param project_path:
        :return:
        """
        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        with open(os.path.join(project_path, 'cpl.json'), 'w') as project_json:
            project_json.write(json.dumps(self._project_json, indent=2))
            project_json.close()

        templates: list[TemplateFileABC] = [
            LicenseTemplate(),
            ReadmeTemplate(),
            TestsInitTemplate()
        ]
        if self._use_application_api:
            templates.append(ApplicationTemplate())
            if self._use_startup:
                templates.append(StartupTemplate())
                templates.append(MainWithApplicationHostAndStartupTemplate())
            else:
                templates.append(MainWithApplicationHostTemplate())
        else:
            templates.append(MainWithoutApplicationHostTemplate())

        for template in templates:
            Console.spinner(
                f'Creating {self._project.name}/{template.path}{template.name}',
                self._create_template,
                project_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )

    @staticmethod
    def _create_template(project_path: str, template: TemplateFileABC):
        """
        Creates template
        :param project_path:
        :param template:
        :return:
        """
        file_path = os.path.join(project_path, template.path, template.name)
        file_rel_path = os.path.join(project_path, template.path)

        if not os.path.isdir(file_rel_path):
            os.makedirs(file_rel_path)

        with open(file_path, 'w') as license_file:
            license_file.write(template.value)
            license_file.close()

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

        self._get_project_informations()
        try:
            self._build_project_dir(path)
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
            exit()

        self._command = args[0]
        if self._command == 'console':
            self._console(args)

        else:
            self._help('Usage: cpl new <schematic> [options]')
            exit()

        Console.write('\n')
