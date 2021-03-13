import json
import os
import sys
from collections import Callable
from typing import Union, Type, Optional

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.configuration.configuration_variable_name_enum import ConfigurationVariableNameEnum
from cpl.configuration.console_argument import ConsoleArgument
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.environment.application_environment import ApplicationEnvironment
from cpl.environment.environment_abc import EnvironmentABC
from cpl.environment.environment_name_enum import EnvironmentNameEnum


class Configuration(ConfigurationABC):

    def __init__(self):
        ConfigurationABC.__init__(self)

        self._hosting_environment = ApplicationEnvironment()
        self._config: dict[Union[type, str], Union[ConfigurationModelABC, str]] = {}

        self._argument_types: list[ConsoleArgument] = []
        self._additional_arguments: list[str] = []

        self._argument_error_function: Optional[Callable] = None

        self._is_multiple_args_allowed = False
        self._handled_args = []

    @property
    def environment(self) -> EnvironmentABC:
        return self._hosting_environment

    @property
    def additional_arguments(self) -> list[str]:
        return self._additional_arguments

    @property
    def argument_error_function(self) -> Optional[Callable]:
        return self._argument_error_function

    @argument_error_function.setter
    def argument_error_function(self, argument_error_function: Callable):
        self._argument_error_function = argument_error_function

    def allow_multiple_args(self):
        self._is_multiple_args_allowed = True

    @staticmethod
    def _print_info(name: str, message: str):
        Console.set_foreground_color(ForegroundColorEnum.green)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    @staticmethod
    def _print_warn(name: str, message: str):
        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    @staticmethod
    def _print_error(name: str, message: str):
        Console.set_foreground_color(ForegroundColorEnum.red)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColorEnum.default)

    def _set_variable(self, name: str, value: str):
        if name == ConfigurationVariableNameEnum.environment.value:
            self._hosting_environment.environment_name = EnvironmentNameEnum(value)

        elif name == ConfigurationVariableNameEnum.name.value:
            self._hosting_environment.application_name = value

        elif name == ConfigurationVariableNameEnum.customer.value:
            self._hosting_environment.customer = value

        else:
            self._config[name] = value

    def _validate_argument_child(self, argument: str, argument_type: ConsoleArgument, next_arguments: Optional[list[str]]) -> bool:
        if argument_type.console_arguments is not None and len(argument_type.console_arguments) > 0:
            found = False
            for child_argument_type in argument_type.console_arguments:
                found = self._validate_argument_by_argument_type(argument, child_argument_type, next_arguments)
                if found and child_argument_type.name not in self._additional_arguments:
                    self._additional_arguments.append(child_argument_type.name)

            if not found:
                raise Exception(f'Invalid argument: {argument}')

            return found

        return True

    def _validate_argument_by_argument_type(self, argument: str, argument_type: ConsoleArgument, next_arguments: list[str] = None) -> bool:
        argument_name = ''
        value = ''
        result = False

        if argument_type.value_token != '' and argument_type.value_token in argument:
            # ?new=value
            if argument_type.is_value_token_optional is not None and argument_type.is_value_token_optional:
                self._additional_arguments.append(argument_type.name)
                result = True

            if not result:
                if argument_type.token != '' and argument.startswith(argument_type.token):
                    # --new=value
                    argument_name = argument.split(argument_type.token)[1].split(argument_type.value_token)[0]
                    value = argument.split(argument_type.token)[1].split(argument_type.value_token)[1]
                else:
                    # new=value
                    argument_name = argument.split(argument_type.token)[1]
                    value = argument.split(argument_type.token)[1].split(argument_type.value_token)[1]

                if argument_name != argument_type.name and argument_name not in argument_type.aliases:
                    return False

                self._set_variable(argument_type.name, value)
                result = True

        elif argument_type.value_token == ' ':
            # ?new value
            if argument_type.is_value_token_optional is not None and argument_type.is_value_token_optional:
                self._additional_arguments.append(argument_type.name)
                result = True

            if not result:
                if next_arguments is None or len(next_arguments) == 0:
                    raise Exception(f'Invalid argument: {argument}')

                value = next_arguments[0]

                if argument_type.token != '' and argument.startswith(argument_type.token):
                    # --new value
                    argument_name = argument.split(argument_type.token)[1]
                else:
                    # new value
                    argument_name = argument

                if argument_name != argument_type.name and argument_name not in argument_type.aliases:
                    return False

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
                result = self._validate_argument_child(next_arguments[0], argument_type, next_args)

        return result

    def add_environment_variables(self, prefix: str):
        for variable in ConfigurationVariableNameEnum.to_list():
            var_name = f'{prefix}{variable}'
            if var_name in [key.upper() for key in os.environ.keys()]:
                self._set_variable(variable, os.environ[var_name])

    def add_console_argument(self, argument: ConsoleArgument):
        self._argument_types.append(argument)

    def add_console_arguments(self):
        for arg_name in ConfigurationVariableNameEnum.to_list():
            self.add_console_argument(ConsoleArgument('--', str(arg_name).upper(), [str(arg_name).lower()], '='))

        arg_list = sys.argv[1:]
        for i in range(0, len(arg_list)):
            argument = arg_list[i]
            next_arguments = []
            error_message = ''

            if argument in self._handled_args:
                break

            if i+1 < len(arg_list):
                next_arguments = arg_list[i+1:]

            found = False
            for argument_type in self._argument_types:
                try:
                    found = self._validate_argument_by_argument_type(argument, argument_type, next_arguments)
                    if found:
                        break
                except Exception as e:
                    error_message = e

            if not found and error_message == '':
                error_message = f'1 Invalid argument: {argument}'

                if self._argument_error_function is not None:
                    self._argument_error_function(error_message)
                else:
                    self._print_error(__name__, error_message)

                exit()

    def add_json_file(self, name: str, optional: bool = None, output: bool = True):
        if self._hosting_environment.content_root_path.endswith('/') and not name.startswith('/'):
            file_path = f'{self._hosting_environment.content_root_path}{name}'
        else:
            file_path = f'{self._hosting_environment.content_root_path}/{name}'

        if not os.path.isfile(file_path):
            if not optional:
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

    def _load_json_file(self, file: str, output: bool) -> dict:
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

    def add_configuration(self, key_type: type, value: ConfigurationModelABC):
        self._config[key_type] = value

    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> Union[str, Callable[ConfigurationModelABC]]:
        if type(search_type) is str:
            if search_type == ConfigurationVariableNameEnum.environment.value:
                return self._hosting_environment.environment_name

            elif search_type == ConfigurationVariableNameEnum.name.value:
                return self._hosting_environment.application_name

            elif search_type == ConfigurationVariableNameEnum.customer.value:
                return self._hosting_environment.customer

        if search_type not in self._config:
            return None

        for config_model in self._config:
            if config_model == search_type:
                return self._config[config_model]
