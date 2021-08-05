from abc import abstractmethod, ABC
from collections import Callable
from typing import Type, Union, Optional

from cpl_core.configuration.console_argument import ConsoleArgument
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class ConfigurationABC(ABC):

    @abstractmethod
    def __init__(self):
        r"""ABC for the :class:`cpl.configuration.configuration.Configuration`"""
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
        r"""Reads the environment variables

        Parameter
        ---------
            prefix: :class:`str`
                Prefix of the variables
        """
        pass

    @abstractmethod
    def add_console_argument(self, argument: ConsoleArgument):
        r"""Adds console argument to known console arguments

        Parameter
        ---------
            argument: :class:`cpl.configuration.console_argument.ConsoleArgument`
                Specifies the console argument
        """
        pass

    @abstractmethod
    def add_console_arguments(self, error: bool = None):
        r"""Reads the console arguments

        Parameter
        ---------
            error: :class:`bool`
                Defines is invalid argument error will be shown or not
        """
        pass

    @abstractmethod
    def add_json_file(self, name: str, optional: bool = None, output: bool = True, path: str = None):
        r"""Reads and saves settings from given json file

        Parameter
        ---------
            name: :class:`str`
                Name of the file
            optional: :class:`str`
                Specifies whether an error should occur if the file was not found
            output: :class:`bool`
                Specifies whether an output should take place
            path: :class:`str`
                Path in which the file should be stored
        """
        pass

    @abstractmethod
    def add_configuration(self, key_type: Union[str, type], value: Union[str, ConfigurationModelABC]):
        r"""Add configuration object

        Parameter
        ---------
            key_type: Union[:class:`str`, :class:`type`]
                Type of the value
            value: Union[:class:`str`, :class:`cpl.configuration.configuration_model_abc.ConfigurationModelABC`]
                Object of the value
        """
        pass

    @abstractmethod
    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> Union[str, Callable[ConfigurationModelABC]]:
        r"""Returns value from configuration by given type

        Parameter
        ---------
            search_type: Union[:class:`str`, Type[:class:`cpl.configuration.configuration_model_abc.ConfigurationModelABC`]]
                Type to search for

        Returns
        -------
            Object of Union[:class:`str`, Callable[:class:`cpl.configuration.configuration_model_abc.ConfigurationModelABC`]]
        """
        pass
