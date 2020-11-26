from abc import ABC, abstractmethod


class ConfigurationModelBase(ABC):

    @abstractmethod
    def from_dict(self, settings: dict): pass
