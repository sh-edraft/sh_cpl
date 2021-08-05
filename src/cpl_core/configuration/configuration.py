import json
import os
import sys
from collections import Callable
from typing import Union, Type, Optional

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.configuration.configuration_variable_name_enum import ConfigurationVariableNameEnum
from cpl_core.configuration.console_argument import ConsoleArgument
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment import ApplicationEnvironment
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.environment.environment_name_enum import EnvironmentNameEnum


class Configuration(ConfigurationABC):

    def __init__(self):
        r"""Representation of configuration"""
        ConfigurationABC.__init__(self)

        self._application_environment = ApplicationEnvironment()
        self._config: dict[Union[type, str], Union[ConfigurationModelABC, str]] = {}

        self._argument_types: list[ConsoleArgument] = []
        self._additional_arguments: list[str] = []

        self._argument_error_function: Optional[Callable] = None

        self._handled_args = []

    @property
    def environment(self) -> ApplicationEnvironmentABC:
        return self._application_environment

    @property
    def additional_arguments(self) -> list[str]:
        return self._additional_arguments

    @property
    def argument_error_function(self) -> Optional[Callable]:
        return self._argument_error_function

    @argument_error_function.setter
    def argument_error_function(self, argument_error_function: Callable):
        self._argument_error_function = argument_error_function

    @staticmethod
    def _print_info(name: str, message: str):
        r"""Prints an info message

        Parameter
        ---------
            name: :class:`str`
                Info name
            message: :class:`str`
                Info message
        """
        Console.set_foreground_color(ForegroundColorEnum.green)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    @staticmethod
    def _print_warn(name: str, message: str):
        r"""Prints a warning

        Parameter
        ---------
            name: :class:`str`
                Warning name
            message: :class:`str`
                Warning message
        """
        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    @staticmethod
    def _print_error(name: str, message: str):
        r"""Prints an error

        Parameter
        ---------
            name: :class:`str`
                Error name
            message: :class:`str`
                Error message
        """
        Console.set_foreground_color(ForegroundColorEnum.red)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    def _set_variable(self, name: str, value: any):
        r"""Sets variable to given value

        Parameter
        ---------
            name: :class:`str`
                Name of the variable
            value: :class:`any`
                Value of the variable
        """
        if name == ConfigurationVariableNameEnum.environment.value:
            self._application_environment.environment_name = EnvironmentNameEnum(value)

        elif name == ConfigurationVariableNameEnum.name.value:
            self._application_environment.application_name = value

        elif name == ConfigurationVariableNameEnum.customer.value:
            self._application_environment.customer = value

        else:
            self._config[name] = value

    def _validate_argument_by_argument_type(self, argument: str, argument_type: ConsoleArgument,
                                            next_arguments: list[str] = None) -> bool:
        r"""Validate argument by argument type

        Parameter
        ---------
            argument: :class:`str`
                Command as string
            argument_type: :class:`cpl.configuration.console_argument.ConsoleArgument`
                Command type as ConsoleArgument
            next_arguments: list[:class:`str`]
                Following arguments of argument

        Returns
        -------
            Object of :class:`bool`

        Raises
        ------
            Exception: An error occurred getting an argument for a command
        """
        argument_name = ''
        value = ''
        result = False

        if argument_type.value_token != '' and argument_type.value_token in argument:
            # ?new=value
            found = False
            for alias in argument_type.aliases:
                if alias in argument:
                    found = True

            if argument_type.name not in argument_name and not found:
                return False

            if argument_type.is_value_token_optional is not None and argument_type.is_value_token_optional:
                if argument_type.name not in self._additional_arguments:
                    self._additional_arguments.append(argument_type.name)
                    result = True

            if argument_type.token != '' and argument.startswith(argument_type.token):
                # --new=value
                if len(argument.split(argument_type.token)[1].split(argument_type.value_token)) == 0:
                    raise Exception(f'Expected argument for command: {argument}')

                argument_name = argument.split(argument_type.token)[1].split(argument_type.value_token)[0]
            else:
                # new=value
                argument_name = argument.split(argument_type.value_token)[1]

            if argument_name == '':
                raise Exception(f'Expected argument for command: {argument_type.name}')

            result = True

            if argument_type.is_value_token_optional is True:
                is_valid = False

                name_list = argument.split(argument_type.token)
                if len(name_list) > 1:
                    value_list = name_list[1].split(argument_type.value_token)
                    if len(value_list) > 1:
                        is_valid = True
                        value = argument.split(argument_type.token)[1].split(argument_type.value_token)[1]

                if not is_valid:
                    if argument_type.name not in self._additional_arguments:
                        self._additional_arguments.append(argument_type.name)
                        result = True
            else:
                value = argument.split(argument_type.token)[1].split(argument_type.value_token)[1]

            if argument_name != argument_type.name and argument_name not in argument_type.aliases:
                return False

            self._set_variable(argument_type.name, value)
            result = True

        elif argument_type.value_token == ' ':
            # ?new value
            found = False
            for alias in argument_type.aliases:
                if alias == argument or f' {alias} ' == argument:
                    found = True

            if argument_type.name not in argument and not found:
                return False

            if (next_arguments is None or len(next_arguments) == 0) and \
                    argument_type.is_value_token_optional is not True:
                raise Exception(f'Expected argument for command: {argument_type.name}')

            if (next_arguments is None or len(next_arguments) == 0) and argument_type.is_value_token_optional is True:
                value = ''
            else:
                value = next_arguments[0]
                next_arguments.remove(value)
                self._handled_args.append(value)

            if argument_type.token != '' and argument.startswith(argument_type.token):
                # --new value
                argument_name = argument.split(argument_type.token)[1]
            else:
                # new value
                argument_name = argument

            if argument_name != argument_type.name and argument_name not in argument_type.aliases:
                return False

            if value == '':
                if argument_type.name not in self._additional_arguments:
                    self._additional_arguments.append(argument_type.name)
            else:
                self._set_variable(argument_type.name, value)

            result = True

        elif argument_type.name == argument or argument in argument_type.aliases:
            # new
            self._additional_arguments.append(argument_type.name)
            result = True

        if result:
            self._handled_args.append(argument)
            if next_arguments is not None and len(next_arguments) > 0:
                next_args = []
                if len(next_arguments) > 1:
                    next_args = next_arguments[1:]

                if argument_type.console_arguments is not None and len(argument_type.console_arguments) > 0:
                    found_child = False
                    for child_argument_type in argument_type.console_arguments:
                        found_child = self._validate_argument_by_argument_type(
                            next_arguments[0],
                            child_argument_type,
                            next_args
                        )
                        if found_child and child_argument_type.name not in self._additional_arguments:
                            self._additional_arguments.append(child_argument_type.name)

                        if found_child:
                            break

                    if not found_child:
                        result = self._validate_argument_by_argument_type(next_arguments[0], argument_type, next_args)

        return result

    def _load_json_file(self, file: str, output: bool) -> dict:
        r"""Reads the json file

        Parameter
        ---------
            file: :class:`str`
                Name of the file
            output: :class:`bool`
                Specifies whether an output should take place

        Returns
        -------
            Object of :class:`dict`
        """
        try:
            # open config file, create if not exists
            with open(file, encoding='utf-8') as cfg:
                # load json
                json_cfg = json.load(cfg)
                if output:
                    self._print_info(__name__, f'Loaded config file: {file}')

                return json_cfg
        except Exception as e:
            self._print_error(__name__, f'Cannot load config file: {file}! -> {e}')
            return {}

    def add_environment_variables(self, prefix: str):
        for variable in ConfigurationVariableNameEnum.to_list():
            var_name = f'{prefix}{variable}'
            if var_name in [key.upper() for key in os.environ.keys()]:
                self._set_variable(variable, os.environ[var_name])

    def add_console_argument(self, argument: ConsoleArgument):
        self._argument_types.append(argument)

    def add_console_arguments(self, error: bool = None):
        for arg_name in ConfigurationVariableNameEnum.to_list():
            self.add_console_argument(ConsoleArgument('--', str(arg_name).upper(), [str(arg_name).lower()], '='))

        arg_list = sys.argv[1:]
        for i in range(0, len(arg_list)):
            argument = arg_list[i]
            next_arguments = []
            error_message = ''

            if argument in self._handled_args:
                break

            if i + 1 < len(arg_list):
                next_arguments = arg_list[i + 1:]

            found = False
            for argument_type in self._argument_types:
                try:
                    found = self._validate_argument_by_argument_type(argument, argument_type, next_arguments)
                    if found:
                        break
                except Exception as e:
                    error_message = e

            if not found and error_message == '' and error is not False:
                error_message = f'Invalid argument: {argument}'

            if error_message != '':
                if self._argument_error_function is not None:
                    self._argument_error_function(error_message)
                else:
                    self._print_error(__name__, error_message)

                exit()

            add_args = []
            for next_arg in next_arguments:
                if next_arg not in self._handled_args and next_arg not in self._additional_arguments:
                    add_args.append(next_arg)

            self._set_variable(f'{argument}AdditionalArguments', add_args)

    def add_json_file(self, name: str, optional: bool = None, output: bool = True, path: str = None):
        if os.path.isabs(name):
            file_path = name
        else:
            path_root = self._application_environment.working_directory
            if path is not None:
                path_root = path

            if str(path_root).endswith('/') and not name.startswith('/'):
                file_path = f'{path_root}{name}'
            else:
                file_path = f'{path_root}/{name}'

        if not os.path.isfile(file_path):
            if optional is not True:
                if output:
                    self._print_error(__name__, f'File not found: {file_path}')

                exit()

            if output:
                self._print_warn(__name__, f'Not Loaded config file: {file_path}')

            return None

        config_from_file = self._load_json_file(file_path, output)
        for sub in ConfigurationModelABC.__subclasses__():
            for key, value in config_from_file.items():
                if sub.__name__ == key or sub.__name__.replace('Settings', '') == key:
                    configuration = sub()
                    configuration.from_dict(value)
                    self.add_configuration(sub, configuration)

    def add_configuration(self, key_type: Union[str, type], value: ConfigurationModelABC):
        self._config[key_type] = value

    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> \
            Union[str, Callable[ConfigurationModelABC]]:
        if type(search_type) is str:
            if search_type == ConfigurationVariableNameEnum.environment.value:
                return self._application_environment.environment_name

            elif search_type == ConfigurationVariableNameEnum.name.value:
                return self._application_environment.application_name

            elif search_type == ConfigurationVariableNameEnum.customer.value:
                return self._application_environment.customer

        if search_type not in self._config:
            return None

        for config_model in self._config:
            if config_model == search_type:
                return self._config[config_model]
