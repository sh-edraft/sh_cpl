import textwrap
from typing import Optional

from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.command_handler_service import CommandHandler
from cpl_cli.command_abc import CommandABC


class HelpService(CommandABC):

    def __init__(self, services: ServiceProviderABC, cmd_handler: CommandHandler):
        """
        Service for CLI command help
        """
        CommandABC.__init__(self)

        self._services = services
        self._commands = cmd_handler.commands

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        """)

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) > 0:
            command_name = args[0]
            command: Optional[CommandABC] = None
            for cmd in self._commands:
                if cmd.name == command_name:
                    command = self._services.get_service(cmd.command)

            if command is None:
                Console.error(f'Invalid argument: {command_name}')

            Console.write_line(command.help_message)

            return

        Console.write_line('Available Commands:')
        commands = [
            ['add (a|a)', 'Adds a project reference to given project.'],
            ['build (b|B)', 'Prepares files for publish into an output directory named dist/ at the given output path. Must be executed from within a workspace directory.'],
            ['generate (g|G)', 'Generate a new file.'],
            ['help (h|H)', 'Lists available command and their short descriptions.'],
            ['install (i|I)', 'With argument installs packages to project, without argument installs project dependencies.'],
            ['new (n|N)', 'Creates new CPL project.'],
            ['publish (p|P)', 'Prepares files for publish into an output directory named dist/ at the given output path and executes setup.py. Must be executed from within a library workspace directory.'],
            ['remove (r|R)', 'Removes a project from workspace.'],
            ['start (s|S)', 'Starts CPL project, restarting on file changes.'],
            ['uninstall (ui|UI)', 'Uninstalls packages from project.'],
            ['update (u|u)', 'Update CPL and project dependencies.'],
            ['version (v|V)', 'Outputs CPL CLI version.']
        ]
        for name, description in commands:
            Console.set_foreground_color(ForegroundColorEnum.blue)
            Console.write(f'\n\t{name} ')
            Console.set_foreground_color(ForegroundColorEnum.default)
            Console.write(f'{description}')
