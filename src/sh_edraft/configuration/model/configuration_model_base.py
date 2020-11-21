from abc import ABC, abstractmethod


class ConfigurationModelBase(ABC):

    @abstractmethod
    def from_dict(self, settings: dict):
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
