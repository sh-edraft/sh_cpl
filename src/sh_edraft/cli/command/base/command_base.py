from abc import ABC, abstractmethod


class CommandBase(ABC):

    @abstractmethod
    def __init__(self):
        self._aliases: list[str] = []

    @property
    def aliases(self):
        return self._aliases

    @abstractmethod
    def run(self, args: list[str]): pass
