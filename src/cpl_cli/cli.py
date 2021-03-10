from typing import Optional

from cpl.application.application_abc import ApplicationABC
from cpl_cli.command.build import Build
from cpl_cli.command.generate import Generate
from cpl_cli.command.new import New
from cpl_cli.command.publish import Publish
from cpl_cli.command_handler import CommandHandler
from cpl_cli.command_model import CommandModel
from cpl_cli.error import Error
from cpl_cli.command.help import Help
from cpl_cli.command.version import Version


class CLI(ApplicationABC):

    def __init__(self):
        ApplicationABC.__init__(self)

        self._command_handler: Optional[CommandHandler] = None

    def configure(self):
        self._command_handler: CommandHandler = self._services.get_service(CommandHandler)

        self._command_handler.add_command(CommandModel('build', ['h', 'B'], Build, True))
        self._command_handler.add_command(CommandModel('generate', ['g', 'G'], Generate, True))
        self._command_handler.add_command(CommandModel('help', ['h', 'H'], Help, False))
        self._command_handler.add_command(CommandModel('new', ['n', 'N'], New, False))
        self._command_handler.add_command(CommandModel('publish', ['p', 'P'], Publish, True))
        self._command_handler.add_command(CommandModel('version', ['v', 'V'], Version, False))

    def main(self):
        if len(self._configuration.additional_arguments) < 1:
            Error.error(f'Expected command')
            return

        self._command_handler.handle(self._configuration.additional_arguments[0], self._configuration.additional_arguments[1:])
