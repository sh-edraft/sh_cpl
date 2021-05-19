from abc import abstractmethod, ABC


class CommandABC(ABC):

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @property
    @abstractmethod
    def help_message(self) -> str: pass

    @abstractmethod
    def run(self, args: list[str]): pass
