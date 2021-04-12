from typing import Optional

from cpl.application.application_abc import ApplicationABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.dependency_injection import ServiceProviderABC
from cpl_cli.command.add_service import AddService
from cpl_cli.command.build_service import BuildService
from cpl_cli.command.generate_service import GenerateService
from cpl_cli.command.install_service import InstallService
from cpl_cli.command.new_service import NewService
from cpl_cli.command.publish_service import PublishService
from cpl_cli.command.remove_service import RemoveService
from cpl_cli.command.start_service import StartService
from cpl_cli.command.uninstall_service import UninstallService
from cpl_cli.command.update_service import UpdateService
from cpl_cli.command_handler_service import CommandHandler
from cpl_cli.command_model import CommandModel
from cpl_cli.error import Error
from cpl_cli.command.help_service import HelpService
from cpl_cli.command.version_service import VersionService


class CLI(ApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        """
        CPL CLI
        """
        ApplicationABC.__init__(self, config, services)

        self._command_handler: Optional[CommandHandler] = None
        self._options: list[str] = []

    def configure(self):
        self._command_handler: CommandHandler = self._services.get_service(CommandHandler)

        self._command_handler.add_command(CommandModel('add', ['a', 'a'], AddService, False, False, False))
        self._command_handler.add_command(CommandModel('build', ['b', 'B'], BuildService, False, True, True))
        self._command_handler.add_command(CommandModel('generate', ['g', 'G'], GenerateService, False, True, False))
        self._command_handler.add_command(CommandModel('help', ['h', 'H'], HelpService, False, False, False))
        self._command_handler.add_command(CommandModel('install', ['i', 'I'], InstallService, False, True, True))
        self._command_handler.add_command(CommandModel('new', ['n', 'N'], NewService, False, False, True))
        self._command_handler.add_command(CommandModel('publish', ['p', 'P'], PublishService, False, True, True))
        self._command_handler.add_command(CommandModel('remove', ['r', 'R'], RemoveService, True, True, False))
        self._command_handler.add_command(CommandModel('start', ['s', 'S'], StartService, False, True, True))
        self._command_handler.add_command(CommandModel('uninstall', ['ui', 'UI'], UninstallService, False, True, True))
        self._command_handler.add_command(CommandModel('update', ['u', 'U'], UpdateService, False, True, True))
        self._command_handler.add_command(CommandModel('version', ['v', 'V'], VersionService, False, False, False))

        self._command_handler.add_command(CommandModel('--help', ['-h', '-H'], HelpService, False, False, False))
        self._options.append('--help')

    def main(self):
        """
        Entry point of the CPL CLI
        :return:
        """
        try:
            command = None
            args = []
            if len(self._configuration.additional_arguments) > 0:
                is_option = False
                for opt in self._options:
                    if opt in self._configuration.additional_arguments:
                        is_option = True
                        command = opt
                        args = self._configuration.additional_arguments
                        args.remove(opt)

                if not is_option:
                    command = self._configuration.additional_arguments[0]
                    if len(self._configuration.additional_arguments) > 1:
                        args = self._configuration.additional_arguments[1:]
            else:
                for cmd in self._command_handler.commands:
                    result = self._configuration.get_configuration(cmd.name)
                    result_args: list[str] = self._configuration.get_configuration(f'{cmd.name}AdditionalArguments')
                    is_option = False
                    for opt in self._options:
                        if opt == result:
                            is_option = True
                            command = opt

                        elif result_args is not None and opt in result_args:
                            is_option = True
                            command = opt
                            result_args.remove(opt)

                    if is_option:
                        args.append(cmd.name)
                        for arg in result_args:
                            args.append(arg)

                    elif result is not None:
                        command = cmd.name
                        args.append(result)

                        for arg in result_args:
                            args.append(arg)

            if command is None:
                Error.error(f'Expected command')
                return

            self._command_handler.handle(command, args)
        except KeyboardInterrupt:
            Console.write_line()
            exit()
