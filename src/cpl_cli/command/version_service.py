import pkgutil
import sys
import platform
import pkg_resources
import textwrap

import cpl_cli
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.command_abc import CommandABC


class VersionService(CommandABC):

    def __init__(self):
        """
        Service for the CLI command version
        """
        CommandABC.__init__(self)

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Lists the version of CPL, CPL CLI and all installed packages from pip.
        Usage: cpl version
        """)

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        packages = []
        cpl_packages = []
        dependencies = dict(tuple(str(ws).split()) for ws in pkg_resources.working_set)
        for p in dependencies:
            if str(p).startswith('cpl-'):
                cpl_packages.append([p, dependencies[p]])
                continue

            packages.append([p, dependencies[p]])

        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.banner('CPL CLI')
        Console.set_foreground_color(ForegroundColorEnum.default)
        if '__version__' in dir(cpl_cli):
            Console.write_line(f'Common Python library CLI: ')
            Console.write(cpl_cli.__version__)

        Console.write_line(f'Python: ')
        Console.write(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        Console.write_line(f'OS: {platform.system()} {platform.processor()}')
        Console.write_line('\nCPL packages:')
        Console.table(['Name', 'Version'], cpl_packages)
        Console.write_line('\nPython packages:')
        Console.table(['Name', 'Version'], packages)
