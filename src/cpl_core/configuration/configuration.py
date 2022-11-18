import json
import os
import sys
import traceback
from collections.abc import Callable
from typing import Union, Type, Optional

from cpl_core.configuration.argument_abc import ArgumentABC
from cpl_core.configuration.argument_builder import ArgumentBuilder
from cpl_core.configuration.argument_executable_abc import ArgumentExecutableABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.configuration.configuration_variable_name_enum import ConfigurationVariableNameEnum
from cpl_core.configuration.executable_argument import ExecutableArgument
from cpl_core.configuration.flag_argument import FlagArgument
from cpl_core.configuration.validator_abc import ValidatorABC
from cpl_core.configuration.variable_argument import VariableArgument
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.dependency_injection.service_provider_abc import ServiceProviderABC
from cpl_core.environment.application_environment import ApplicationEnvironment
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.environment.environment_name_enum import EnvironmentNameEnum


class Configuration(ConfigurationABC):

    def __init__(self):
        r"""Representation of configuration"""
        ConfigurationABC.__init__(self)

        self._application_environment = ApplicationEnvironment()
        self._config: dict[Union[type, str], Union[ConfigurationModelABC, str]] = {}

        self._argument_types: list[ArgumentABC] = []
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

    @property
    def arguments(self) -> list[ArgumentABC]:
        return self._argument_types

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

    def _handle_pre_or_post_executables(self, pre: bool, argument: ExecutableArgument, services: ServiceProviderABC):
        script_type = 'pre-' if pre else 'post-'

        from cpl_cli.configuration.workspace_settings import WorkspaceSettings
        workspace: Optional[WorkspaceSettings] = self.get_configuration(WorkspaceSettings)
        if workspace is None or len(workspace.scripts) == 0:
            return

        for script in workspace.scripts:
            if script_type not in script and not script.startswith(script_type):
                continue

            # split in two ifs to prevent exception
            if script.split(script_type)[1] != argument.name:
                continue

            from cpl_cli.command.custom_script_service import CustomScriptService
            css: CustomScriptService = services.get_service(CustomScriptService)
            if css is None:
                continue

            Console.write_line()
            self._set_variable('ACTIVE_EXECUTABLE', script)
            css.run(self._additional_arguments)

    def _parse_arguments(self, executables: list[ArgumentABC], arg_list: list[str], args_types: list[ArgumentABC]):
        for i in range(0, len(arg_list)):
            arg_str = arg_list[i]
            for n in range(0, len(args_types)):
                arg = args_types[n]
                arg_str_without_token = arg_str
                if arg.token != "" and arg.token in arg_str:
                    arg_str_without_token = arg_str.split(arg.token)[1]

                # executable
                if isinstance(arg, ExecutableArgument):
                    if arg_str.startswith(arg.token) and arg_str_without_token == arg.name or arg_str_without_token in arg.aliases:
                        executables.append(arg)
                        self._handled_args.append(arg_str)
                        self._parse_arguments(executables, arg_list[i + 1:], arg.console_arguments)

                # variables
                elif isinstance(arg, VariableArgument):
                    arg_str_without_value = arg_str_without_token
                    if arg.value_token in arg_str_without_value:
                        arg_str_without_value = arg_str_without_token.split(arg.value_token)[0]

                    if arg_str.startswith(arg.token) and arg_str_without_value == arg.name or arg_str_without_value in arg.aliases:
                        if arg.value_token != ' ':
                            value = arg_str_without_token.split(arg.value_token)[1]
                        else:
                            value = arg_list[i + 1]
                        self._set_variable(arg.name, value)
                        self._handled_args.append(arg_str)
                        self._handled_args.append(value)
                        self._parse_arguments(executables, arg_list[i + 1:], arg.console_arguments)

                # flags
                elif isinstance(arg, FlagArgument):
                    if arg_str.startswith(arg.token) and arg_str_without_token == arg.name or arg_str_without_token in arg.aliases:
                        if arg_str in self._additional_arguments:
                            self._additional_arguments.remove(arg_str)
                        self._additional_arguments.append(arg.name)
                        self._handled_args.append(arg_str)
                        self._parse_arguments(executables, arg_list[i + 1:], arg.console_arguments)

            # add left over values to args
            if arg_str not in self._additional_arguments and arg_str not in self._handled_args:
                self._additional_arguments.append(arg_str)

    def add_environment_variables(self, prefix: str):
        for env_var in os.environ.keys():
            if not env_var.startswith(prefix):
                continue

            self._set_variable(env_var.replace(prefix, ''), os.environ[env_var])

    def add_console_argument(self, argument: ArgumentABC):
        self._argument_types.append(argument)

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

                sys.exit()

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

    def add_configuration(self, key_type: Union[str, type], value: Union[str, ConfigurationModelABC]):
        self._config[key_type] = value

    def create_console_argument(self, arg_type: ArgumentTypeEnum, token: str, name: str, aliases: list[str],
                                *args, **kwargs) -> ArgumentABC:
        argument = ArgumentBuilder.build_argument(arg_type, token, name, aliases, *args, **kwargs)
        self._argument_types.append(argument)
        return argument

    def for_each_argument(self, call: Callable):
        for arg in self._argument_types:
            call(arg)

    def get_configuration(self, search_type: Union[str, Type[ConfigurationModelABC]]) -> \
            Optional[Union[str, ConfigurationModelABC]]:
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

    def parse_console_arguments(self, services: ServiceProviderABC, error: bool = None) -> bool:
        # sets environment variables as possible arguments as: --VAR=VALUE
        for arg_name in ConfigurationVariableNameEnum.to_list():
            self.add_console_argument(VariableArgument('--', str(arg_name).upper(), [str(arg_name).lower()], '='))

        success = False
        try:
            arg_list = sys.argv[1:]
            executables: list[ExecutableArgument] = []
            self._parse_arguments(executables, arg_list, self._argument_types)
        except Exception as e:
            Console.error('An error occurred while parsing arguments.')
            sys.exit()

        try:
            prevent = False
            for exe in executables:
                if prevent:
                    continue

                if exe.validators is not None:
                    abort = False
                    for validator_type in exe.validators:
                        validator: ValidatorABC = services.get_service(validator_type)
                        result = validator.validate()
                        abort = not result
                        if abort:
                            break

                    if abort:
                        sys.exit()

                cmd: ArgumentExecutableABC = services.get_service(exe.executable_type)
                self._handle_pre_or_post_executables(True, exe, services)
                self._set_variable('ACTIVE_EXECUTABLE', exe.name)
                cmd.execute(self._additional_arguments)
                self._handle_pre_or_post_executables(False, exe, services)
                prevent = exe.prevent_next_executable
                success = True
        except Exception as e:
            Console.error('An error occurred while executing arguments.', traceback.format_exc())
            sys.exit()

        return success
