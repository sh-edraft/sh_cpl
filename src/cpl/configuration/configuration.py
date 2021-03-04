import json
import os
import sys
from collections import Callable
from typing import Union, Type, Optional

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.configuration.configuration_variable_name import ConfigurationVariableName
from cpl.configuration.console_argument import ConsoleArgument
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl.environment.hosting_environment import HostingEnvironment
from cpl.environment.environment_abc import EnvironmentABC
from cpl.environment.environment_name import EnvironmentName


class Configuration(ConfigurationABC):

    def __init__(self):
        ConfigurationABC.__init__(self)

        self._hosting_environment = HostingEnvironment()
        self._config: dict[Union[type, str], Union[ConfigurationModelABC, str]] = {}

        self._argument_types: list[ConsoleArgument] = []
        self._additional_arguments: list[str] = []

        self._argument_error_function: Optional[Callable] = None

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

    @staticmethod
    def _print_info(name: str, message: str):
        Console.set_foreground_color(ForegroundColor.green)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColor.default)

    @staticmethod
    def _print_warn(name: str, message: str):
        Console.set_foreground_color(ForegroundColor.yellow)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColor.default)

    @staticmethod
    def _print_error(name: str, message: str):
        Console.set_foreground_color(ForegroundColor.red)
        Console.write_line(f'[{name}] {message}')
        Console.set_foreground_color(ForegroundColor.default)

    def _set_variable(self, name: str, value: str):
        if name == ConfigurationVariableName.environment.value:
            self._hosting_environment.environment_name = EnvironmentName(value)

        elif name == ConfigurationVariableName.name.value:
            self._hosting_environment.application_name = value

        elif name == ConfigurationVariableName.customer.value:
            self._hosting_environment.customer = value

        else:
            self._config[name] = value

    def add_environment_variables(self, prefix: str):
        for variable in ConfigurationVariableName.to_list():
            var_name = f'{prefix}{variable}'
            if var_name in [key.upper() for key in os.environ.keys()]:
                self._set_variable(variable, os.environ[var_name])

    def add_console_argument(self, token: str, name: str, aliases: list[str], value_token: str):
        self._argument_types.append(ConsoleArgument(token, name, aliases, value_token))

    def add_console_arguments(self):
        for arg_name in ConfigurationVariableName.to_list():
            self.add_console_argument('--', arg_name, [], '')

        for arg in sys.argv[1:]:
            try:
                is_done = False
                for argument_type in self._argument_types:
                    # check prefix
                    if argument_type.token != '' and arg.startswith(argument_type.token):
                        name = arg.split(argument_type.token)[1]

                        if argument_type.value_token == '':
                            if name == argument_type.name or name in argument_type.aliases:
                                self._additional_arguments.append(argument_type.name)
                                is_done = True
                                break

                        if argument_type.value_token != '' and arg.__contains__(argument_type.value_token):
                            name = name.split(argument_type.value_token)[0]
                            if name == argument_type.name or name in argument_type.aliases:
                                value = arg.split(argument_type.value_token)[1]
                                self._set_variable(argument_type.name, value)
                                is_done = True
                                break

                    elif argument_type.value_token == '' and arg == argument_type.name or arg in argument_type.aliases:
                        is_done = True
                        self._additional_arguments.append(argument_type.name)
                        break

                if not is_done:
                    message = f'Invalid argument: {arg}'

                    if self._argument_error_function is not None:
                        self._argument_error_function(message)
                    else:
                        self._print_error(__name__, message)

                    exit()
            except Exception as e:
                message = f'Invalid argument: {arg} -> {e}'

                if self._argument_error_function is not None:
                    self._argument_error_function(message)
                else:
                    self._print_error(__name__, message)

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
                if sub.__name__ == key:
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
        if search_type not in self._config:
            raise Exception(f'Config model by type {search_type} not found')

        for config_model in self._config:
            if config_model == search_type:
                return self._config[config_model]
