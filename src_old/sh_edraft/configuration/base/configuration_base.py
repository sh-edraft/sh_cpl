from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.environment.base.environment_base import EnvironmentBase


class ConfigurationBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def environment(self) -> EnvironmentBase: pass

    @abstractmethod
    def add_environment_variables(self, prefix: str): pass

    @abstractmethod
    def add_argument_variables(self): pass

    @abstractmethod
    def add_json_file(self, name: str, optional: bool = None): pass

    @abstractmethod
    def add_configuration(self, key_type: type, value: object): pass

    @abstractmethod
    def get_configuration(self, search_type: Type[ConfigurationModelBase]) -> Callable[ConfigurationModelBase]: pass

    @abstractmethod
    def create(self): pass
