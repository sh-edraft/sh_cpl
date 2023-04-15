from abc import abstractmethod

from cpl_core.type import T


class Observer:
    def __init__(self):
        pass

    @abstractmethod
    def next(self, value: T):
        pass

    @abstractmethod
    def error(self, ex: Exception):
        pass

    @abstractmethod
    def complete(self):
        pass
