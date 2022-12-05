from abc import ABC, abstractmethod


class ArgumentExecutableABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def run(self, args: list[str]): pass
