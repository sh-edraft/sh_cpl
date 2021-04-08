import json
import os
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl.utils.string import String
from cpl_cli.configuration.workspace_settings_name_enum import WorkspaceSettingsNameEnum
from cpl_cli.source_creator.template_builder import TemplateBuilder
from cpl_cli.templates.new.library.appsettings_json import AppsettingsTemplate
from cpl_cli.templates.new.library.license import LicenseTemplate
from cpl_cli.templates.new.library.readme_py import ReadmeTemplate
from cpl_cli.templates.new.library.src.name.application import ApplicationTemplate
from cpl_cli.templates.new.library.src.name.init import NameInitTemplate
from cpl_cli.templates.new.library.src.name.main import MainWithApplicationHostAndStartupTemplate, \
    MainWithoutApplicationBaseTemplate, MainWithApplicationBaseTemplate, MainWithDependencyInjection
from cpl_cli.templates.new.library.src.name.startup import StartupTemplate
from cpl_cli.templates.new.library.src.tests.init import TestsInitTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class LibraryBuilder:

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
              project_name: str, project_settings: dict):
        """
        Builds the library project files
        :param project_path:
        :param use_application_api:
        :param use_startup:
        :param use_service_providing:
        :param project_name:
        :param project_settings:
        :return:
        """
        if not os.path.isdir(project_path):
            os.makedirs(project_path)

        templates: list[TemplateFileABC] = [
            LicenseTemplate(),
            ReadmeTemplate(),
            TestsInitTemplate(),
            NameInitTemplate(project_name),
            AppsettingsTemplate()
        ]

        if use_application_api:
            templates.append(ApplicationTemplate(project_name))

            if use_startup:
                templates.append(StartupTemplate(project_name))
                templates.append(MainWithApplicationHostAndStartupTemplate(project_name))
            else:
                templates.append(MainWithApplicationBaseTemplate(project_name))
        else:
            if use_service_providing:
                templates.append(MainWithDependencyInjection())
            else:
                templates.append(MainWithoutApplicationBaseTemplate())

        workspace_file_path = f'{project_name}/cpl-workspace.json'
        project_file_rel_path = f'src/{String.convert_to_snake_case(project_name)}/{project_name}.json'
        Console.spinner(
            f'Creating {workspace_file_path}',
            cls._create_file,
            workspace_file_path,
            {
                WorkspaceSettingsNameEnum.default_project.value: project_name,
                WorkspaceSettingsNameEnum.projects.value: {
                    project_name: project_file_rel_path
                }
            },
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        project_file_path = f'{project_name}/{project_file_rel_path}'
        Console.spinner(
            f'Creating {project_file_path}',
            cls._create_file,
            project_file_path,
            project_settings,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        for template in templates:
            Console.spinner(
                f'Creating {project_name}/{template.path}{template.name}',
                TemplateBuilder.build,
                project_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )
