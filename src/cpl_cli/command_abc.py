from abc import abstractmethod, ABC

from cpl_core.configuration.executable_argument import ExecutableArgument


class CommandABC(ExecutableArgument):

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @property
    @abstractmethod
    def help_message(self) -> str: pass
