from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.dependency_injection.service_abc import ServiceABC
from cpl.dependency_injection.service_provider_base import ServiceProviderABC
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
                self._services.get_service(command.command).run(args)
