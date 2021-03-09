import json
import os
import sys
from distutils.dir_util import copy_tree

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name import BuildSettingsName
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name import ProjectSettingsName
from cpl_cli.configuration.version_settings_name import VersionSettingsName


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

    def _create_project_dir(self):
        project_path = os.path.join(self._runtime.working_directory, self._project.name)
        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.error('Project path is not empty\n')
            exit()

        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        with open(os.path.join(project_path, 'cpl.json'), 'w') as project_json:
            project_json.write(json.dumps(self._project_json, indent=4))
            project_json.close()

        template_path = os.path.join(self._runtime.runtime_directory, f'templates/new/{self._command}')
        if not os.path.isdir(template_path):
            Console.error(template_path, '\n\nTemplate path not found\n')
            exit()

        copy_tree(template_path, project_path)

    def _console(self, args: list[str]):
        name = self._config.get_configuration(self._command)
        self._create_project_settings(name)
        self._create_build_settings()
        self._create_project_json()
        self._create_project_dir()

    def run(self, args: list[str]):
        self._command = args[0]
        if self._command == 'console':
            self._console(args)
