import pkgutil
import sys
import platform
import pkg_resources
import textwrap

import cpl_cli
import cpl_core
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

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
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
        cpl_packages = [
            'cpl_core',
            'cpl_cli',
            'cpl_query'
        ]
        packages = []
        for modname in cpl_packages:
            module = pkgutil.find_loader(modname)
            if module is None:
                break
            
            module = module.load_module(modname)
            if '__version__' in dir(module):
                packages.append([f'{modname}', module.__version__])

        Console.table(['Name', 'Version'], packages)

        Console.write_line('\nPython packages:')
        packages = []
        dependencies = dict(tuple(str(ws).split()) for ws in pkg_resources.working_set)
        for p in dependencies:
            packages.append([p, dependencies[p]])

        Console.table(['Name', 'Version'], packages)
