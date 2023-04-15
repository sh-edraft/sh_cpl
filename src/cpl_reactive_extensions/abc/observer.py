from abc import abstractmethod, ABC

from cpl_core.type import T


class Observer(ABC):
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def next(self, value: T):
        pass

    @abstractmethod
    def error(self, ex: Exception):
        pass

    @abstractmethod
    def complete(self):
        pass
