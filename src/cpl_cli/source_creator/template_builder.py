import json
import os

from cpl_cli.abc.file_template_abc import FileTemplateABC
from cpl_cli.configuration import WorkspaceSettings, WorkspaceSettingsNameEnum
from cpl_core.console import Console, ForegroundColorEnum


class TemplateBuilder:
    @staticmethod
    def build_cpl_file(file_name: str, content: dict):
        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)

        path = os.path.dirname(file_name)
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(file_name, "w") as project_json:
            project_json.write(json.dumps(content, indent=2))
            project_json.close()

    @classmethod
    def create_workspace(cls, path: str, project_name, projects: dict, scripts: dict):
        ws_dict = {
            WorkspaceSettings.__name__: {
                WorkspaceSettingsNameEnum.default_project.value: project_name,
                WorkspaceSettingsNameEnum.projects.value: projects,
                WorkspaceSettingsNameEnum.scripts.value: scripts,
            }
        }

        Console.spinner(
            f"Creating {path}",
            cls.build_cpl_file,
            path,
            ws_dict,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan,
        )

    @staticmethod
    def build(file_path: str, template: FileTemplateABC):
        """
        Creates template
        :param file_path:
        :param template:
        :return:
        """
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        with open(file_path, "w") as file:
            file.write(template.value)
            file.close()
