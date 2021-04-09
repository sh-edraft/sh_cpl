import os
from abc import ABC
from typing import Optional

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
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

    def _load_json(self):
        pass

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
                    self._config.add_json_file('cpl-workspace.json', optional=True, output=False)
                    workspace = self._config.get_configuration(WorkspaceSettings)

                if command.is_project_needed:
                    if os.path.isfile(
                            os.path.join(
                                self._env.working_directory,
                                f'{os.path.basename(self._env.working_directory)}.json'
                            )
                    ):
                        project_name = os.path.basename(self._env.working_directory)

                    if workspace is None and project_name is None:
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
                        Error.error(
                            'The command requires to be run in an CPL project, but a project could not be found.'
                        )
                        return

                    project_json = os.path.join(self._env.working_directory, project_json)

                    self._env.set_working_directory(
                        os.path.join(self._env.working_directory, os.path.dirname(project_json))
                    )

                    self._config.add_json_file(project_json, optional=True, output=False)

                self._services.get_service(command.command).run(args)
                Console.write('\n')
