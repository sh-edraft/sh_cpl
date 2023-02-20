import sys
import textwrap

from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_cli.command_abc import CommandABC


class HelpService(CommandABC):
    def __init__(self, services: ServiceProviderABC):
        """
        Service for CLI command help
        """
        CommandABC.__init__(self)

        self._services = services

    @property
    def help_message(self) -> str:
        return textwrap.dedent(
            """\
        Lists available command and their short descriptions.
        Usage: cpl help
        """
        )

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) > 0:
            Console.error(f'Unexpected argument(s): {", ".join(args)}')
            sys.exit()

        Console.write_line("Available Commands:")
        commands = [
            ["add (a|a)", "Adds a project reference to given project."],
            [
                "build (b|B)",
                "Prepares files for publish into an output directory named dist/ at the given output path. Must be executed from within a workspace directory.",
            ],
            ["generate (g|G)", "Generate a new file."],
            ["help (h|H)", "Lists available command and their short descriptions."],
            [
                "install (i|I)",
                "With argument installs packages to project, without argument installs project dependencies.",
            ],
            ["new (n|N)", "Creates new CPL project."],
            [
                "publish (p|P)",
                "Prepares files for publish into an output directory named dist/ at the given output path and executes setup.py. Must be executed from within a library workspace directory.",
            ],
            ["remove (r|R)", "Removes a project from workspace."],
            ["start (s|S)", "Starts CPL project, restarting on file changes."],
            ["uninstall (ui|UI)", "Uninstalls packages from project."],
            ["update (u|u)", "Update CPL and project dependencies."],
            ["version (v|V)", "Outputs CPL CLI version."],
        ]
        for name, description in commands:
            Console.set_foreground_color(ForegroundColorEnum.blue)
            Console.write(f"\n\t{name} ")
            Console.set_foreground_color(ForegroundColorEnum.default)
            Console.write(f"{description}")
        Console.write_line("\nRun 'cpl <command> --help' for command specific information's\n")
