import json
import os
import sys

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.configuration.configuration_model_abc import ConfigurationModelABC
from cpl.configuration.configuration_variable_name import ConfigurationVariableName
from cpl.console.console import Console
from cpl.console.foreground_color import ForegroundColor
from cpl.environment.hosting_environment import HostingEnvironment
from cpl.environment.environment_abc import EnvironmentABC
from cpl.environment.environment_name import EnvironmentName


class Configuration(ConfigurationABC):

    def __init__(self):
        ConfigurationABC.__init__(self)

        self._hosting_environment = HostingEnvironment()
        self._config: dict[type, ConfigurationModelABC] = {}

    @property
    def environment(self) -> EnvironmentABC:
        return self._hosting_environment

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

    def add_environment_variables(self, prefix: str):
        for variable in ConfigurationVariableName.to_list():
            var_name = f'{prefix}{variable}'
            if var_name in [key.upper() for key in os.environ.keys()]:
                self._set_variable(variable, os.environ[var_name])

    def add_argument_variables(self):
        for arg in sys.argv[1:]:
            try:
                argument = arg.split('--')[1].split('=')[0].upper()
                value = arg.split('=')[1]

                if argument not in ConfigurationVariableName.to_list():
                    raise Exception(f'Invalid argument name: {argument}')

                self._set_variable(argument, value)
            except Exception as e:
                self._print_error(__name__, f'Invalid argument: {arg} -> {e}')
                exit()

    def add_json_file(self, name: str, optional: bool = None):
        if self._hosting_environment.content_root_path.endswith('/') and not name.startswith('/'):
            file_path = f'{self._hosting_environment.content_root_path}{name}'
        else:
            file_path = f'{self._hosting_environment.content_root_path}/{name}'

        if not os.path.isfile(file_path):
            if not optional:
                self._print_error(__name__, f'File not found: {file_path}')
                exit()

            self._print_warn(__name__, f'Not Loaded config file: {file_path}')
            return None

        config_from_file = self._load_json_file(file_path)
        for sub in ConfigurationModelABC.__subclasses__():
            for key, value in config_from_file.items():
                if sub.__name__ == key:
                    configuration = sub()
                    configuration.from_dict(value)
                    self.add_configuration(sub, configuration)

    def _load_json_file(self, file: str) -> dict:
        try:
            # open config file, create if not exists
            with open(file, encoding='utf-8') as cfg:
                # load json
                json_cfg = json.load(cfg)
                self._print_info(__name__, f'Loaded config file: {file}')
                return json_cfg
        except Exception as e:
            self._print_error(__name__, f'Cannot load config file: {file}! -> {e}')
            return {}

    def add_configuration(self, key_type: type, value: ConfigurationModelABC):
        self._config[key_type] = value

    def get_configuration(self, search_type: type) -> ConfigurationModelABC:
        if search_type not in self._config:
            raise Exception(f'Config model by type {search_type} not found')

        for config_model in self._config:
            if config_model == search_type:
                return self._config[config_model]
