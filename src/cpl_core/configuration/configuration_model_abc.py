from abc import ABC, abstractmethod


def base_func(method):
    method.is_base_func = True
    return method


class ConfigurationModelABC(ABC):
    @abstractmethod
    def __init__(self):
        r"""ABC for settings representation"""
        pass

    @base_func
    def from_dict(self, settings: dict):
        r"""Converts attributes to dict

        Parameter:
            settings: :class:`dict`
        """
        pass
