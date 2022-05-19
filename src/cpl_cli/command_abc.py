from abc import abstractmethod, ABC

from cpl_core.configuration.executable_argument import ExecutableArgument
from cpl_core.console import Console


class CommandABC(ExecutableArgument):

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @property
    @abstractmethod
    def help_message(self) -> str: pass

    def execute(self, args: list[str]):
        if 'help' in args:
            Console.write_line(self.help_message)
            return

        self.run(args)

    @abstractmethod
    def run(self, args: list[str]): pass
