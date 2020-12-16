from abc import ABC, abstractmethod

from sh_edraft.console.console import Console


class CommandBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def run(self, args: list[str]): pass
