import os

from cpl.application.application_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console import ForegroundColor
from cpl.console.console import Console
from cpl.utils.string import String
from cpl_cli.command_abc import CommandABC
from cpl_cli.templates.generate.abc_template import ABCTemplate


class Generate(CommandABC):

    def __init__(self, configuration: ConfigurationABC, runtime: ApplicationRuntimeABC):
        CommandABC.__init__(self)

        self._config = configuration
        self._runtime = runtime

    @staticmethod
    def _help(message: str):
        Console.error(message)

        schematics = [
            ['abc (a|A)'],
            ['class (c|C)'],
            ['configmodel (cm|CM)'],
            ['enum (e|E)'],
            ['service (s|S)'],
        ]
        Console.write_line('Available Schematics:')
        for name in schematics:
            Console.write(f'\n\t{name} ')

    @staticmethod
    def _create_file(file_path: str, value: str):
        with open(file_path, 'w') as template:
            template.write(value)
            template.close()

    def _generate_abc(self, name: str):
        rel_path = ''
        if '/' in name:
            parts = name.split('/')
            rel_path = '/'.join(parts[:-1])
            name = parts[len(parts) - 1]

        file_path = os.path.join(self._runtime.working_directory, rel_path, f'{String.convert_to_snake_case(name)}.py')
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        if os.path.isfile(file_path):
            Console.error('ABC already exists!')
            exit()

        message = f'Creating {self._runtime.working_directory}/{rel_path}/{String.convert_to_snake_case(name)}.py'
        if rel_path == '':
            message = f'Creating {self._runtime.working_directory}/{String.convert_to_snake_case(name)}.py'

        Console.spinner(
            message,
            self._create_file,
            file_path,
            ABCTemplate.get_abc_py(name),
            text_foreground_color=ForegroundColor.green,
            spinner_foreground_color=ForegroundColor.cyan
        )

    def run(self, args: list[str]):
        if len(args) == 0:
            self._help('Usage: cpl generate <schematic> [options]')
            exit()

        schematic = args[0]
        name = self._config.get_configuration(schematic)
        if name is None:
            name = Console.read(f'Name for the {args[0]}: ')

        if schematic == 'abc':
            self._generate_abc(name)

        elif schematic == 'class':
            pass

        elif schematic == 'configmodel':
            pass

        elif schematic == 'enum':
            pass

        elif schematic == 'service':
            pass

        else:
            self._help('Usage: cpl generate <schematic> [options]')
            exit()

        Console.write('\n')
