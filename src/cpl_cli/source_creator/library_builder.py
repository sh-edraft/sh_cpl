import json
import os
from typing import Optional

from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.console.console import Console
from cpl_core.utils.string import String
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.configuration.workspace_settings_name_enum import WorkspaceSettingsNameEnum
from cpl_cli.source_creator.template_builder import TemplateBuilder
from cpl_cli._templates.new.library.appsettings_json import AppsettingsTemplate
from cpl_cli._templates.new.library.license import LicenseTemplate
from cpl_cli._templates.new.library.readme_py import ReadmeTemplate
from cpl_cli._templates.new.library.source.name.application import ApplicationTemplate
from cpl_cli._templates.new.library.source.name.init import NameInitTemplate
from cpl_cli._templates.new.library.source.name.main import MainWithApplicationHostAndStartupTemplate, \
    MainWithoutApplicationBaseTemplate, MainWithApplicationBaseTemplate, MainWithDependencyInjection
from cpl_cli._templates.new.library.source.name.startup import StartupTemplate
from cpl_cli._templates.new.library.source.tests.init import TestsInitTemplate
from cpl_cli._templates.template_file_abc import TemplateFileABC


class LibraryBuilder:

    def __init__(self):
        pass

    @staticmethod
    def _create_file(file_name: str, content: dict):
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)

        path = os.path.dirname(file_name)
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(file_name, 'w') as project_json:
            project_json.write(json.dumps(content, indent=2))
            project_json.close()

    @classmethod
    def _create_workspace(cls, path: str, project_name, projects: dict, scripts: dict):
        ws_dict = {
            WorkspaceSettings.__name__: {
                WorkspaceSettingsNameEnum.default_project.value: project_name,
                WorkspaceSettingsNameEnum.projects.value: projects,
                WorkspaceSettingsNameEnum.scripts.value: scripts,
            }
        }

        Console.spinner(
            f'Creating {path}',
            cls._create_file,
            path,
            ws_dict,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

    @classmethod
    def build(cls, project_path: str, use_application_api: bool, use_startup: bool,
              use_async: bool, use_service_providing: bool, project_name: str, project_settings: dict,
              workspace: Optional[WorkspaceSettings]):
        """
        Builds the library project files
        :param project_path:
        :param use_application_api:
        :param use_startup:
        :param use_service_providing:
        :param use_async:
        :param project_name:
        :param project_settings:
        :param workspace:
        :return:
        """
        pj_name = project_name
        if '/' in pj_name:
            pj_name = pj_name.split('/')[len(pj_name.split('/')) - 1]

        project_name_snake = String.convert_to_snake_case(pj_name)

        if workspace is None:
            templates: list[TemplateFileABC] = [
                LicenseTemplate(),
                ReadmeTemplate(),
                TestsInitTemplate(),
                NameInitTemplate(project_name, os.path.join(
                    'src/', project_name_snake)),
                AppsettingsTemplate()
            ]
        else:
            project_path = os.path.join(
                os.path.dirname(project_path),
                project_name_snake
            )

            templates: list[TemplateFileABC] = [
                LicenseTemplate(),
                ReadmeTemplate(),
                NameInitTemplate('', ''),
                AppsettingsTemplate()
            ]

        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        src_rel_path = ''
        src_name = project_name_snake

        if use_application_api:
            templates.append(ApplicationTemplate(
                src_name, src_rel_path, use_async))

            if use_startup:
                templates.append(StartupTemplate(
                    src_name, src_rel_path, use_async))
                templates.append(MainWithApplicationHostAndStartupTemplate(
                    src_name, src_rel_path, use_async))
            else:
                templates.append(MainWithApplicationBaseTemplate(
                    src_name, src_rel_path, use_async))
        else:
            if use_service_providing:
                templates.append(MainWithDependencyInjection(
                    src_name, src_rel_path, use_async))
            else:
                templates.append(MainWithoutApplicationBaseTemplate(
                    src_name, src_rel_path, use_async))

        if '/' in project_name:
            old_pj_name = project_name
            parts = project_name.split('/')
            project_name = parts[len(parts) - 1]
            src_rel_path = old_pj_name.split(project_name)[0]

        proj_name = project_name
        if src_rel_path.endswith('/'):
            src_rel_path = src_rel_path[:len(src_rel_path) - 1]
        
        if src_rel_path != '':
            proj_name = f'{src_rel_path}/{project_name}'
        if workspace is not None:
            proj_name = project_name_snake

        if src_rel_path != '':
            project_file_path = f'{src_rel_path}/{project_name_snake}/{project_name}.json'
        else:
            project_file_path = f'{project_name_snake}/{project_name}.json'

        if workspace is None:
            src_path = f'src/{project_name_snake}'
            workspace_file_path = f'{proj_name}/cpl-workspace.json'
            project_file_rel_path = f'{src_path}/{project_name}.json'
            project_file_path = f'{proj_name}/{src_path}/{project_name}.json'
            cls._create_workspace(
                workspace_file_path,
                project_name, 
                {
                    project_name: project_file_rel_path
                },
                {}
            )

        else:
            workspace.projects[project_name] = f'src/{project_file_path}'
            cls._create_workspace('cpl-workspace.json', workspace.default_project, workspace.projects, workspace.scripts)

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
            if template.path != '' and not template.path.endswith('/'):
                divider = '/'

            Console.spinner(
                f'Creating {proj_name}/{template.path}{divider}{template.name}',
                TemplateBuilder.build,
                project_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )
