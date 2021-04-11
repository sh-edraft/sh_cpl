from abc import abstractmethod, ABC
from collections import Callable
from typing import Type, Union, Optional

from cpl.configuration.console_argument import ConsoleArgument
from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.environment.application_environment_abc import ApplicationEnvironmentABC


class ConfigurationABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC of configuration
        """
        pass

    @property
    @abstractmethod
    def environment(self) -> ApplicationEnvironmentABC: pass

    @property
    @abstractmethod
    def additional_arguments(self) -> list[str]: pass

    @property
    @abstractmethod
    def argument_error_function(self) -> Optional[Callable]: pass

    @argument_error_function.setter
    @abstractmethod
    def argument_error_function(self, argument_error_function: Callable): pass

    @abstractmethod
    def add_environment_variables(self, prefix: str):
        """
        Reads the environment variables
        :param prefix:
        :return:
        """
        pass

    @abstractmethod
    def add_console_argument(self, argument: ConsoleArgument):
        """
        Adds console argument to known console arguments
        :param argument:
        :return:
        """
        pass

    @abstractmethod
    def add_console_arguments(self, error: bool = None):
        """
        Reads the console arguments
        :param error: defines is invalid argument error will be shown or not
        :return:
        """
        pass

    @abstractmethod
    def add_json_file(self, name: str, optional: bool = None, output: bool = True, path: str = None):
        """
        Reads and saves settings from given json file
        :param name:
        :param optional:
        :param output:
        :param path:
        :return:
        """
        pass

    @abstractmethod
    def add_configuration(self, key_type: Union[str, type], value: object):
        """
        Add configuration object
        :param key_type:
        :param value:
        :return:
        """
        pass

    @abstractmethod
    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> Union[str, Callable[ConfigurationModelABC]]:
        """
        Returns value in configuration by given type
        :param search_type:
        :return:
        """
        pass
