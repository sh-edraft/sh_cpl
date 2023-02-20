from abc import ABC, abstractmethod


class ConfigurationModelABC(ABC):
    @abstractmethod
    def __init__(self):
        r"""ABC for settings representation"""
        pass

    @abstractmethod
    def from_dict(self, settings: dict):
        r"""Converts attributes to dict

        Parameter:
            settings: :class:`dict`
        """
        pass
