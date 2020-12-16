import pkgutil
import sys
import platform

import sh_edraft
from sh_edraft import cli
from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.console.console import Console


class Version(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)

    def run(self, args: list[str]):
        Console.set_foreground_color('yellow')
        Console.banner('CPL CLI')
        Console.set_foreground_color('default')
        Console.write_line(f'Common Python Library CLI: {cli.__version__}')
        Console.write_line(f'Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')
        Console.write_line(f'OS: {platform.system()} {platform.processor()}')

        Console.write_line('\nCPL:')
        packages = []
        for importer, modname, is_pkg in pkgutil.iter_modules(sh_edraft.__path__):
            module = importer.find_module(modname).load_module(modname)
            packages.append([f'{modname}:', module.__version__])

        Console.table(['Name', 'Version'], packages)
