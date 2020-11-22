from abc import ABC, abstractmethod


class ServiceBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def init(self, args: tuple): pass

    @abstractmethod
    def create(self): pass
