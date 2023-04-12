from cpl_core.configuration import ArgumentExecutableABC
from cpl_core.console import Console


class InstallArgument(ArgumentExecutableABC):
    def __init__(self):
        ArgumentExecutableABC.__init__(self)

    def execute(self, args: list[str]):
        Console.write_line("Install:", args)
