from abc import abstractmethod, ABC


class CommandABC(ABC):

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def run(self, args: list[str]): pass
