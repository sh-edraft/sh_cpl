from abc import ABC, abstractmethod


class ServiceBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def create(self): pass
