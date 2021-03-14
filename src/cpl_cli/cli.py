from typing import Optional

from cpl.application.application_abc import ApplicationABC
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command_handler_service import CommandHandler
from cpl_cli.command_model import CommandModel
from cpl_cli.error import Error
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.version_service import VersionService


class CLI(ApplicationABC):

    def __init__(self):
        """
        CPL CLI
        """
        ApplicationABC.__init__(self)

        self._command_handler: Optional[CommandHandler] = None

    def configure(self):
        self._command_handler: CommandHandler = self._services.get_service(CommandHandler)

        self._command_handler.add_command(CommandModel('build', ['h', 'B'], BuildService, True))
        self._command_handler.add_command(CommandModel('generate', ['g', 'G'], GenerateService, True))
        self._command_handler.add_command(CommandModel('help', ['h', 'H'], HelpService, False))
        self._command_handler.add_command(CommandModel('install', ['i', 'I'], InstallService, False))
        self._command_handler.add_command(CommandModel('new', ['n', 'N'], NewService, False))
        self._command_handler.add_command(CommandModel('publish', ['p', 'P'], PublishService, True))
        self._command_handler.add_command(CommandModel('start', ['s', 'S'], StartService, True))
        self._command_handler.add_command(CommandModel('uninstall', ['ui', 'UI'], UninstallService, True))
        self._command_handler.add_command(CommandModel('update', ['u', 'U'], UpdateService, True))
        self._command_handler.add_command(CommandModel('version', ['v', 'V'], VersionService, False))

    def main(self):
        """
        Entry point of the CPL CLI
        :return:
        """
        command = None
        args = []
        if len(self._configuration.additional_arguments) > 0:
            command = self._configuration.additional_arguments[0]
            if len(self._configuration.additional_arguments) > 1:
                args = self._configuration.additional_arguments[1:]
        else:
            for cmd in self._command_handler.commands:
                result = self._configuration.get_configuration(cmd.name)
                if result is not None:
                    command = cmd.name
                    args.append(result)

        if command is None:
            Error.error(f'Expected command')
            return

        self._command_handler.handle(command, args)
