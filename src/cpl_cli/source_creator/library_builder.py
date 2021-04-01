import json
import os
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl_cli.source_creator.template_builder import TemplateBuilder
from cpl_cli.templates.new.library.appsettings_json import AppsettingsTemplate
from cpl_cli.templates.new.library.license import LicenseTemplate
from cpl_cli.templates.new.library.readme_py import ReadmeTemplate
from cpl_cli.templates.new.library.src.cli.application import ApplicationTemplate
from cpl_cli.templates.new.library.src.cli.init import CLIInitTemplate
from cpl_cli.templates.new.library.src.cli.main import MainWithApplicationHostAndStartupTemplate, \
    MainWithoutApplicationBaseTemplate, MainWithApplicationBaseTemplate, MainWithDependencyInjection
from cpl_cli.templates.new.library.src.cli.startup import StartupTemplate
from cpl_cli.templates.new.library.src.tests.init import TestsInitTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class LibraryBuilder:

    def __init__(self):
        pass

    @staticmethod
    def build(project_path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool,
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

        with open(os.path.join(project_path, 'cpl.json'), 'w') as project_json:
            project_json.write(json.dumps(project_settings, indent=2))
            project_json.close()

        templates: list[TemplateFileABC] = [
            LicenseTemplate(),
            ReadmeTemplate(),
            TestsInitTemplate(),
            CLIInitTemplate(project_name),
            AppsettingsTemplate()
        ]

        if use_application_api:
            templates.append(ApplicationTemplate(project_name))

            if use_startup:
                templates.append(StartupTemplate(project_name))
                templates.append(MainWithApplicationHostAndStartupTemplate(project_name))
            else:
                templates.append(MainWithApplicationBaseTemplate())
        else:
            if use_service_providing:
                templates.append(MainWithDependencyInjection())
            else:
                templates.append(MainWithoutApplicationBaseTemplate())

        for template in templates:
            Console.spinner(
                f'Creating {project_name}/{template.path}{template.name}',
                TemplateBuilder.build,
                project_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )
