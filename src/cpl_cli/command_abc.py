from abc import abstractmethod, ABC

from cpl_core.configuration.argument_executable_abc import ArgumentExecutableABC
from cpl_core.console import Console


class CommandABC(ArgumentExecutableABC):
    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @property
    @abstractmethod
    def help_message(self) -> str:
        pass

    @abstractmethod
    def execute(self, args: list[str]):
        pass

    def run(self, args: list[str]):
        if "help" in args:
            Console.write_line(self.help_message)
            return

        self.execute(args)
