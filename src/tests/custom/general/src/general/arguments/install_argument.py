from cpl_core.configuration.runnable_argument_abc import RunnableArgumentABC
from cpl_core.console import Console


class InstallArgument(RunnableArgumentABC):

    def __init__(self):
        RunnableArgumentABC.__init__(self)

    def run(self, args: list[str]):
        Console.write_line('Install:', args)
