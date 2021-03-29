import os

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection.service_abc import ServiceABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.error import Error
from cpl_cli.command_model import CommandModel


class CommandHandler(ServiceABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        """
        Service to handle incoming commands and args
        :param config:
        :param services:
        """
        ServiceABC.__init__(self)

        self._config = config
        self._env = self._config.environment
        self._services = services

        self._commands: list[CommandModel] = []

    @property
    def commands(self) -> list[CommandModel]:
        return self._commands

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
                if command.is_project_needed and not os.path.isfile(os.path.join(self._env.working_directory, 'cpl.json')):
                    Error.error('The command requires to be run in an CPL project, but a project could not be found.')
                    return

                if command.is_project_needed:
                    self._config.add_json_file('cpl.json', optional=True, output=False)

                self._services.get_service(command.command).run(args)
                Console.write('\n')
