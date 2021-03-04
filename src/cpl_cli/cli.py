from typing import Optional

from cpl.application.application_abc import ApplicationABC
from cpl_cli.command import Command
from cpl_cli.command_handler import CommandHandler
from cpl_cli.error import Error
from cpl_cli.commands.help import Help
from cpl_cli.commands.version import Version


class CLI(ApplicationABC):

    def __init__(self):
        ApplicationABC.__init__(self)

        self._command_handler: Optional[CommandHandler] = None

    def configure(self):
        self._command_handler: CommandHandler = self._services.get_service(CommandHandler)

        self._command_handler.add_command(Command('help', ['h', 'H'], self._services.get_service(Help)))
        self._command_handler.add_command(Command('version', ['v', 'V'], self._services.get_service(Version)))

    def main(self):
        if len(self._configuration.additional_arguments) < 1:
            Error.error(f'Expected command')
            return

        self._command_handler.handle(self._configuration.additional_arguments[0], self._configuration.additional_arguments[1:])
