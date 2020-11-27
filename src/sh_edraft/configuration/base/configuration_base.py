from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase


class ConfigurationBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def add_config_by_type(self, key_type: type, value: object): pass

    @abstractmethod
    def get_config_by_type(self, search_type: Type[ConfigurationModelBase]) -> Callable[ConfigurationModelBase]: pass

    @abstractmethod
    def create(self): pass
