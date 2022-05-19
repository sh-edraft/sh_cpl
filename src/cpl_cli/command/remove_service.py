import os
import shutil
import json
import textwrap

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import WorkspaceSettings, WorkspaceSettingsNameEnum


class RemoveService(CommandABC):

    def __init__(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        """
        Service for CLI command remove
        :param config:
        :param env:
        """
        CommandABC.__init__(self)

        self._config = config
        self._env = env

        self._workspace: WorkspaceSettings = self._config.get_configuration(WorkspaceSettings)
        self._is_simulation = False

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Removes a project from workspace.
        Usage: cpl remove <project>
        
        Arguments:
            project     The name of the project to delete
        """)

    def _create_file(self, file_name: str, content: dict):
        if self._is_simulation:
            return

        if not os.path.isabs(file_name):
            file_name = os.path.abspath(file_name)

        path = os.path.dirname(file_name)
        if not os.path.isdir(path):
            os.makedirs(path)

        with open(file_name, 'w') as project_json:
            project_json.write(json.dumps(content, indent=2))
            project_json.close()

    @staticmethod
    def _remove_sources(path: str):
        shutil.rmtree(path)

    def _create_workspace(self, path: str):
        ws_dict = {
            WorkspaceSettings.__name__: {
                WorkspaceSettingsNameEnum.default_project.value: self._workspace.default_project,
                WorkspaceSettingsNameEnum.projects.value: self._workspace.projects,
                WorkspaceSettingsNameEnum.scripts.value: self._workspace.scripts
            }
        }

        self._create_file(path, ws_dict)

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if 'simulate' in args:
            args.remove('simulate')
            Console.write_line('Simulating:')
            self._is_simulation = True

        project_name = args[0]
        if project_name not in self._workspace.projects:
            Console.error(f'Project {project_name} not found in workspace.')
            return

        if project_name == self._workspace.default_project:
            Console.error(f'Project {project_name} is the default project.')
            return

        src_path = os.path.abspath(os.path.dirname(self._workspace.projects[project_name]))
        Console.spinner(
            f'Removing {src_path}',
            self._remove_sources,
            src_path,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        del self._workspace.projects[project_name]
        path = 'cpl-workspace.json'
        Console.spinner(
            f'Changing {path}',
            self._create_workspace,
            path,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
