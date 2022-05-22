from cpl_core.configuration.argument_executable_abc import ArgumentExecutableABC
from cpl_core.console import Console


class InstallArgument(ArgumentExecutableABC):

    def __init__(self):
        ArgumentExecutableABC.__init__(self)

    def run(self, args: list[str]):
        Console.write_line('Install:', args)
