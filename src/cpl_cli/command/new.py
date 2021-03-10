import json
import os
import sys
import time
from typing import Optional

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.foreground_color import ForegroundColor
from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name import BuildSettingsName
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name import ProjectSettingsName
from cpl_cli.configuration.version_settings_name import VersionSettingsName
from cpl_cli.templates.new.console.license import LicenseTemplate
from cpl_cli.templates.new.console.readme_py import ReadmeTemplate
from cpl_cli.templates.new.console.src.application import ApplicationTemplate
from cpl_cli.templates.new.console.src.main import MainWithApplicationHostAndStartupTemplate, MainWithoutApplicationHostTemplate, MainWithApplicationHostTemplate
from cpl_cli.templates.new.console.src.startup import StartupTemplate
from cpl_cli.templates.new.console.src.tests.init import TestsInitTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class New(CommandABC):

    def __init__(self, configuration: ConfigurationABC, runtime: ApplicationRuntimeABC):
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

    def _create_project_settings(self, name: str):
        self._project_dict = {
            ProjectSettingsName.name.value: name,
            ProjectSettingsName.version.value: {
                VersionSettingsName.major.value: '0',
                VersionSettingsName.minor.value: '0',
                VersionSettingsName.micro.value: '0'
            },
            ProjectSettingsName.author.value: '',
            ProjectSettingsName.author_email.value: '',
            ProjectSettingsName.description.value: '',
            ProjectSettingsName.long_description.value: '',
            ProjectSettingsName.url.value: '',
            ProjectSettingsName.copyright_date.value: '',
            ProjectSettingsName.copyright_name.value: '',
            ProjectSettingsName.license_name.value: '',
            ProjectSettingsName.license_description.value: '',
            ProjectSettingsName.dependencies.value: [],
            ProjectSettingsName.python_version.value: f'>={sys.version.split(" ")[0]}'
        }

        self._project.from_dict(self._project_dict)

    def _create_build_settings(self):
        self._build_dict = {
            BuildSettingsName.source_path.value: 'src',
            BuildSettingsName.output_path.value: 'dist',
            BuildSettingsName.main.value: 'main',
            BuildSettingsName.entry_point.value: self._project.name,
            BuildSettingsName.include_package_data.value: 'False',
            BuildSettingsName.included.value: [],
            BuildSettingsName.excluded.value: [
                '*/__pycache__',
                '*/logs',
                '*/tests'
            ],
            BuildSettingsName.package_data.value: {}
        }
        self._build.from_dict(self._build_dict)

    def _create_project_json(self):
        self._project_json = {
            ProjectSettings.__name__: self._project_dict,
            BuildSettings.__name__: self._build_dict
        }

    def _get_project_path(self) -> Optional[str]:
        project_path = os.path.join(self._runtime.working_directory, self._project.name)
        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.error('Project path is not empty\n')
            return None

        return project_path

    def _get_project_informations(self):
        result = Console.read('Do you want to use application host? (y/n) ')
        if result.lower() == 'y':
            self._use_application_api = True

        if self._use_application_api:
            result = Console.read('Do you want to use startup? (y/n) ')
            if result.lower() == 'y':
                self._use_startup = True

        Console.set_foreground_color(ForegroundColor.default)

        # else:
        #     result = Console.read('Do you want to use service providing? (y/n) ')
        #     if result.lower() == 'y':
        #         self._use_service_providing = True

    def _build_project_dir(self, project_path: str):
        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        with open(os.path.join(project_path, 'cpl.json'), 'w') as project_json:
            project_json.write(json.dumps(self._project_json, indent=4))
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
                text_foreground_color=ForegroundColor.green,
                spinner_foreground_color=ForegroundColor.cyan
            )

    @staticmethod
    def _create_template(project_path: str, template: TemplateFileABC):
        file_path = os.path.join(project_path, template.path, template.name)
        file_rel_path = os.path.join(project_path, template.path)

        if not os.path.isdir(file_rel_path):
            os.makedirs(file_rel_path)

        with open(file_path, 'w') as license_file:
            license_file.write(template.value)
            license_file.close()

    def _console(self, args: list[str]):
        name = self._config.get_configuration(self._command)

        self._create_project_settings(name)
        self._create_build_settings()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_informations()
        try:
            self._build_project_dir(path)
        except Exception as e:
            Console.error('Could not create project', str(e))

    def run(self, args: list[str]):
        self._command = args[0]
        if self._command == 'console':
            self._console(args)

        Console.write('\n')
