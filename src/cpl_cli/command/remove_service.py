import os
import shutil
import json
import textwrap

from cpl_cli.configuration.settings_helper import SettingsHelper

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import WorkspaceSettings, WorkspaceSettingsNameEnum, BuildSettingsNameEnum, ProjectSettings, BuildSettings


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

    def _remove_sources(self, path: str):
        if self._is_simulation:
            return
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

    def _get_project_settings(self, project: str) -> dict:
        with open(os.path.join(os.getcwd(), self._workspace.projects[project]), 'r', encoding='utf-8') as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        return project_json

    def _write_project_settings(self, project: str, project_settings: dict, build_settings: dict):
        with open(os.path.join(os.getcwd(), self._workspace.projects[project]), 'w', encoding='utf-8') as file:
            file.write(json.dumps({
                ProjectSettings.__name__: project_settings,
                BuildSettings.__name__: build_settings
            }, indent=2))
            file.close()

    def _find_deps_in_projects(self, project_name: str, rel_path: str):
        for project in self._workspace.projects:
            if project == project_name:
                continue

            project_settings = self._get_project_settings(project)
            if BuildSettings.__name__ not in project_settings or BuildSettingsNameEnum.project_references.value not in project_settings[BuildSettings.__name__]:
                continue

            ref_to_delete = ''
            for ref in project_settings[BuildSettings.__name__][BuildSettingsNameEnum.project_references.value]:
                if os.path.basename(ref) == f'{project_name}.json':
                    ref_to_delete = ref

            if ref_to_delete not in project_settings[BuildSettings.__name__][BuildSettingsNameEnum.project_references.value]:
                continue

            project_settings[BuildSettings.__name__][BuildSettingsNameEnum.project_references.value].remove(ref_to_delete)
            Console.spinner(
                f'Removing {project_name} from {project}',
                self._write_project_settings,
                project,
                project_settings[ProjectSettings.__name__],
                project_settings[BuildSettings.__name__],
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan
            )

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if 'simulate' in args:
            args.remove('simulate')
            Console.write_line('Running in simulation mode:')
            self._is_simulation = True

        project_name = args[0]
        if project_name not in self._workspace.projects:
            Console.error(f'Project {project_name} not found in workspace.')
            return

        if project_name == self._workspace.default_project:
            Console.error(f'Project {project_name} is the default project.')
            return

        src_path = os.path.dirname(self._workspace.projects[project_name])
        Console.spinner(
            f'Removing {src_path}',
            self._remove_sources,
            os.path.abspath(src_path),
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

        self._find_deps_in_projects(project_name, src_path)

        del self._workspace.projects[project_name]
        path = 'cpl-workspace.json'
        Console.spinner(
            f'Changing {path}',
            self._create_workspace,
            path,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
