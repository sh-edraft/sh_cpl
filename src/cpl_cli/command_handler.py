from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.dependency_injection.service_abc import ServiceABC
from cpl_cli.command import Command


class CommandHandler(ServiceABC):

    def __init__(self, runtime: ApplicationRuntimeABC):
        ServiceABC.__init__(self)

        self._runtime = runtime

        self._commands: list[Command] = []

    def add_command(self, cmd: Command):
        self._commands.append(cmd)

    def remove_command(self, cmd: Command):
        self._commands.remove(cmd)

    def handle(self, cmd: str, args: list[str]):
        for command in self._commands:
            if cmd == command.name or cmd in command.aliases:
                command.command.run(args)
