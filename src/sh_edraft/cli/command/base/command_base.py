from abc import ABC, abstractmethod


class CommandBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def run(self, args: list[str]): pass
