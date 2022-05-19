from abc import abstractmethod, ABC
from collections.abc import Callable
from typing import Type, Union, Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.configuration.argument_abc import ArgumentABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class ConfigurationABC(ABC):

    @abstractmethod
    def __init__(self):
        r"""ABC for the :class:`cpl_core.configuration.configuration.Configuration`"""
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

    @property
    @abstractmethod
    def arguments(self) -> list[ArgumentABC]: pass

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
    def add_console_argument(self, argument: ArgumentABC):
        r"""Adds console argument to known console arguments

        Parameter
        ---------
            argument: :class:`cpl_core.configuration.console_argument.ConsoleArgumentABC`
                Specifies the console argument
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
            value: Union[:class:`str`, :class:`cpl_core.configuration.configuration_model_abc.ConfigurationModelABC`]
                Object of the value
        """
        pass

    @abstractmethod
    def create_console_argument(self, arg_type: ArgumentTypeEnum, token: str, name: str, aliases: list[str],
                                *args, **kwargs) -> ArgumentABC:
        r"""Creates and adds a console argument to known console arguments

        Parameter
        ---------
            token: :class:`str`
                Specifies optional beginning of argument
            name :class:`str`
                Specifies name of argument
            aliases list[:class:`str`]
                Specifies possible aliases of name
            value_token :class:`str`
                Specifies were the value begins
            is_value_token_optional :class:`bool`
                Specifies if values are optional
            runnable: :class:`cpl_core.configuration.console_argument.ConsoleArgumentABC`
                Specifies class to run when called if value is not None

        Returns
        ------
            Object of :class:`cpl_core.configuration.console_argument.ConsoleArgumentABC`
        """
        pass

    @abstractmethod
    def for_each_argument(self, call: Callable):
        r"""Iterates through all arguments and calls the call function

        Parameter
        ---------
            call: :class:`Callable`
                Call for each argument
        """
        pass

    @abstractmethod
    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> Union[
        str, ConfigurationModelABC]:
        r"""Returns value from configuration by given type

        Parameter
        ---------
            search_type: Union[:class:`str`, Type[:class:`cpl_core.configuration.configuration_model_abc.ConfigurationModelABC`]]
                Type to search for

        Returns
        -------
            Object of Union[:class:`str`, :class:`cpl_core.configuration.configuration_model_abc.ConfigurationModelABC`]
        """
        pass

    @abstractmethod
    def parse_console_arguments(self, services: 'ServiceProviderABC', error: bool = None):
        r"""Reads the console arguments

        Parameter
        ---------
            error: :class:`bool`
                Defines is invalid argument error will be shown or not
        """
        pass
