from abc import abstractmethod, ABC
from collections import Callable
from typing import Type

from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.environment.environment_abc import EnvironmentABC


class ConfigurationABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def environment(self) -> EnvironmentABC: pass

    @abstractmethod
    def add_environment_variables(self, prefix: str): pass

    @abstractmethod
    def add_argument_variables(self): pass

    @abstractmethod
    def add_json_file(self, name: str, optional: bool = None): pass

    @abstractmethod
    def add_configuration(self, key_type: type, value: object): pass

    @abstractmethod
    def get_configuration(self, search_type: Type[ConfigurationModelABC]) -> Callable[ConfigurationModelABC]: pass
