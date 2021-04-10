import json
import os
from typing import Optional

from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl.utils.string import String
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.configuration.workspace_settings_name_enum import WorkspaceSettingsNameEnum
from cpl_cli.source_creator.template_builder import TemplateBuilder
from cpl_cli.templates.new.console.appsettings_json import AppsettingsTemplate
from cpl_cli.templates.new.console.license import LicenseTemplate
from cpl_cli.templates.new.console.readme_py import ReadmeTemplate
from cpl_cli.templates.new.console.source.name.application import ApplicationTemplate
from cpl_cli.templates.new.console.source.name.init import MainInitTemplate
from cpl_cli.templates.new.console.source.name.main import MainWithApplicationHostAndStartupTemplate, \
    MainWithoutApplicationBaseTemplate, MainWithApplicationBaseTemplate, MainWithDependencyInjection
from cpl_cli.templates.new.console.source.name.startup import StartupTemplate
from cpl_cli.templates.new.console.source.tests.init import TestsInitTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class ConsoleBuilder:

    def __init__(self):
        pass

    @staticmethod
    def _create_file(file_name: str, content: dict):
        path = os.path.dirname(file_name)
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(file_name, 'w') as project_json:
            project_json.write(json.dumps(content, indent=2))
            project_json.close()

    @classmethod
    def build(cls, project_path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool,
              project_name: str, project_settings: dict, workspace: Optional[WorkspaceSettings]):
        """
        Builds the console project files
        :param project_path:
        :param use_application_api:
        :param use_startup:
        :param use_service_providing:
        :param project_name:
        :param project_settings:
        :param workspace:
        :return:
        """
        project_name_snake = String.convert_to_snake_case(project_name)

        if workspace is None:
            templates: list[TemplateFileABC] = [
                LicenseTemplate(),
                ReadmeTemplate(),
                TestsInitTemplate(),
                AppsettingsTemplate(),
                MainInitTemplate(project_name, 'src')
            ]
        else:
            project_path = os.path.join(
                os.path.dirname(project_path),
                project_name_snake
            )

            templates: list[TemplateFileABC] = [
                LicenseTemplate(),
                ReadmeTemplate(),
                AppsettingsTemplate(),
                MainInitTemplate('', '')
            ]

        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        src_rel_path = ''
        src_name = ''
        if workspace is None:
            src_rel_path = 'src/'
            src_name = project_name_snake

        if use_application_api:
            templates.append(ApplicationTemplate(src_name, src_rel_path))

            if use_startup:
                templates.append(StartupTemplate(src_name, src_rel_path))
                templates.append(MainWithApplicationHostAndStartupTemplate(src_name, src_rel_path))
            else:
                templates.append(MainWithApplicationBaseTemplate(src_name, src_rel_path))
        else:
            if use_service_providing:
                templates.append(MainWithDependencyInjection(src_name, src_rel_path))
            else:
                templates.append(MainWithoutApplicationBaseTemplate(src_name, src_rel_path))

        proj_name = project_name
        if workspace is not None:
            proj_name = project_name_snake

        project_file_path = f'{project_name_snake}/{project_name}.json'
        if workspace is None:
            src_path = f'{proj_name}/src/{project_name_snake}'
            workspace_file_path = f'{proj_name}/cpl-workspace.json'
            project_file_path = f'{src_path}/{project_name}.json'

            Console.spinner(
                f'Creating {workspace_file_path}',
                cls._create_file,
                workspace_file_path,
                {
                    WorkspaceSettings.__name__: {
                        WorkspaceSettingsNameEnum.default_project.value: project_name,
                        WorkspaceSettingsNameEnum.projects.value: {
                            project_name: project_file_path
                        }
                    }
                },
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )

        Console.spinner(
            f'Creating {project_file_path}',
            cls._create_file,
            project_file_path if workspace is None else f'src/{project_file_path}',
            project_settings,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        for template in templates:
            divider = ''
            if not template.path.endswith('/'):
                divider = '/'

            Console.spinner(
                f'Creating {proj_name}/{template.path}{divider}{template.name}',
                TemplateBuilder.build,
                project_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )
