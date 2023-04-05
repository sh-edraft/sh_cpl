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
        r"""DEPRECATED: Set attributes as typed arguments in __init__ instead. See https://docs.sh-edraft.de/cpl/deprecated.html#ConfigurationModelABC-from_dict-method for further information
        Converts attributes to dict

        Parameter:
            settings: :class:`dict`
        """
        pass
