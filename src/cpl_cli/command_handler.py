import os

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.dependency_injection.service_abc import ServiceABC
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.error import Error
from cpl_cli.command_model import CommandModel


class CommandHandler(ServiceABC):

    def __init__(self, runtime: ApplicationRuntimeABC, services: ServiceProviderABC):
        ServiceABC.__init__(self)

        self._runtime = runtime
        self._services = services

        self._commands: list[CommandModel] = []

    def add_command(self, cmd: CommandModel):
        self._commands.append(cmd)

    def remove_command(self, cmd: CommandModel):
        self._commands.remove(cmd)

    def handle(self, cmd: str, args: list[str]):
        for command in self._commands:
            if cmd == command.name or cmd in command.aliases:
                if command.is_project_needed and not os.path.isfile(os.path.join(self._runtime.working_directory, 'cpl.json')):
                    Error.error('The command requires to be run in an CPL project, but a project could not be found.')
                    return

                self._services.get_service(command.command).run(args)
