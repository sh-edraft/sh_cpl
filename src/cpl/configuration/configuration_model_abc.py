from abc import ABC, abstractmethod


class ConfigurationModelABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for settings representation
        """
        pass

    @abstractmethod
    def from_dict(self, settings: dict):
        """
        Converts attributes to dict
        :param settings:
        :return:
        """
        pass
