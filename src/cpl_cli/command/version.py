import os
import pkgutil
import sys
import platform
import pkg_resources

import cpl
import cpl_cli
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl_cli.command_abc import CommandABC


class Version(CommandABC):

    def __init__(self):
        CommandABC.__init__(self)

    def run(self, args: list[str]):
        Console.set_foreground_color(ForegroundColor.yellow)
        Console.banner('CPL CLI')
        Console.set_foreground_color('default')
        if '__version__' in dir(cpl_cli):
            Console.set_foreground_color(ForegroundColor.yellow)
            Console.write_line(f'Common Python Library CLI: ')
            Console.set_foreground_color(ForegroundColor.default)
            Console.write(cpl_cli.__version__)

        Console.set_foreground_color(ForegroundColor.blue)
        Console.write_line(f'Python: ')
        Console.set_foreground_color(ForegroundColor.default)
        Console.write(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')

        Console.write_line(f'OS: {platform.system()} {platform.processor()}')

        Console.set_foreground_color(ForegroundColor.yellow)
        Console.write_line('\nCPL packages:')
        Console.set_foreground_color(ForegroundColor.default)
        packages = []
        for importer, modname, is_pkg in pkgutil.iter_modules(cpl.__path__):
            module = importer.find_module(modname).load_module(modname)
            if '__version__' in dir(module):
                packages.append([f'{modname}', module.__version__])

        Console.table(['Name', 'Version'], packages)

        Console.set_foreground_color(ForegroundColor.blue)
        Console.write_line('\nPython packages:')
        Console.set_foreground_color(ForegroundColor.default)
        packages = []
        dependencies = dict(tuple(str(ws).split()) for ws in pkg_resources.working_set)
        for p in dependencies:
            packages.append([p, dependencies[p]])

        Console.table(['Name', 'Version'], packages)
