from abc import ABC, abstractmethod


class ConfigurationModelABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def from_dict(self, settings: dict): pass
