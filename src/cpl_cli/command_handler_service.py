import os
from abc import ABC
from typing import Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.utils.string import String
from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.error import Error
from cpl_cli.command_model import CommandModel


class CommandHandler(ABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        """
        Service to handle incoming commands and args
        :param config:
        :param services:
        """
        ABC.__init__(self)

        self._config = config
        self._env = self._config.environment
        self._services = services

        self._commands: list[CommandModel] = []

    @property
    def commands(self) -> list[CommandModel]:
        return self._commands

    @staticmethod
    def _project_not_found():
        Error.error(
            'The command requires to be run in an CPL project, but a project could not be found.'
        )

    def add_command(self, cmd: CommandModel):
        self._commands.append(cmd)

    def remove_command(self, cmd: CommandModel):
        self._commands.remove(cmd)

    def handle(self, cmd: str, args: list[str]):
        """
        Handles incoming commands and args
        :param cmd:
        :param args:
        :return:
        """
        for command in self._commands:
            if cmd == command.name or cmd in command.aliases:
                error = None
                project_name: Optional[str] = None
                workspace: Optional[WorkspaceSettings] = None

                if os.path.isfile(os.path.join(self._env.working_directory, 'cpl-workspace.json')):
                    workspace = self._config.get_configuration(WorkspaceSettings)

                if command.is_project_needed:
                    name = os.path.basename(self._env.working_directory)
                    for r, d, f in os.walk(self._env.working_directory):
                        for file in f:
                            if file.endswith('.json'):
                                f_name = file.split('.json')[0]
                                if f_name == name or \
                                        String.convert_to_camel_case(f_name).lower() == String.convert_to_camel_case(
                                    name).lower():
                                    project_name = f_name
                                    break

                    if not command.is_workspace_needed and project_name is None and workspace is None:
                        self._project_not_found()
                        return

                    elif command.is_workspace_needed or project_name is None:
                        if workspace is None:
                            Error.error(
                                'The command requires to be run in an CPL workspace or project, '
                                'but a workspace or project could not be found.'
                            )
                            return

                        if project_name is None:
                            project_name = workspace.default_project

                    self._config.add_configuration('ProjectName', project_name)
                    project_json = f'{project_name}.json'

                    if workspace is not None:
                        if project_name not in workspace.projects:
                            Error.error(
                                f'Project {project_name} not found.'
                            )
                            return
                        project_json = workspace.projects[project_name]

                    if not os.path.isfile(os.path.join(self._env.working_directory, project_json)):
                        self._project_not_found()
                        return

                    project_json = os.path.join(self._env.working_directory, project_json)

                    if command.change_cwd:
                        self._env.set_working_directory(
                            os.path.join(self._env.working_directory, os.path.dirname(project_json))
                        )

                    self._config.add_json_file(project_json, optional=True, output=False)

                # pre scripts
                Console.write('\n')
                self._handle_pre_or_post_scripts(True, workspace, command)
                self._services.get_service(command.command).run(args)
                # post scripts
                Console.write('\n\n')
                self._handle_pre_or_post_scripts(False, workspace, command)
                Console.write('\n')

    def _handle_pre_or_post_scripts(self, pre: bool, workspace: WorkspaceSettings, command: CommandModel):
        script_type = 'pre-' if pre else 'post-'
        if workspace is not None and len(workspace.scripts) > 0:
            for script in workspace.scripts:
                if script_type in script and script.split(script_type)[1] == command.name:
                    script_name = script
                    script_cmd = workspace.scripts[script]
                    if script_cmd in workspace.scripts:
                        script_name = workspace.scripts[script]

                    css: CustomScriptService = self._services.get_service(CustomScriptService)
                    if css is None:
                        continue

                    css.run([script_name])
