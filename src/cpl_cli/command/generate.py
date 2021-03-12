import os
from collections import Callable

from cpl.application.application_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.foreground_color import ForegroundColor
from cpl.console.console import Console
from cpl.utils.string import String
from cpl_cli.command_abc import CommandABC
from cpl_cli.templates.generate.abc_template import ABCTemplate
from cpl_cli.templates.generate.class_template import ClassTemplate
from cpl_cli.templates.generate.configmodel_template import ConfigModelTemplate
from cpl_cli.templates.generate.enum_template import EnumTemplate
from cpl_cli.templates.generate.service_template import ServiceTemplate
from cpl_cli.templates.template_file_abc import TemplateFileABC


class Generate(CommandABC):

    def __init__(self, configuration: ConfigurationABC, runtime: ApplicationRuntimeABC):
        CommandABC.__init__(self)

        self._schematics = {
            "abc": {
                "Upper": "ABC",
                "Template": ABCTemplate
            },
            "class": {
                "Upper": "Class",
                "Template": ClassTemplate
            },
            "configmodel": {
                "Upper": "Settings",
                "Template": ConfigModelTemplate
            },
            "enum": {
                "Upper": "Enum",
                "Template": EnumTemplate
            },
            "service": {
                "Upper": "Service",
                "Template": ServiceTemplate
            }
        }

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

    def _generate(self, schematic: str, name: str, template: Callable[TemplateFileABC]):
        class_name = name
        rel_path = ''
        if '/' in name:
            parts = name.split('/')
            rel_path = '/'.join(parts[:-1])
            class_name = parts[len(parts) - 1]

        template = template(class_name, schematic, self._schematics[schematic]["Upper"], rel_path)

        file_path = os.path.join(self._runtime.working_directory, template.path, template.name)
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        if os.path.isfile(file_path):
            Console.error(f'{String.first_to_upper(schematic)} already exists!')
            exit()

        message = f'Creating {self._runtime.working_directory}/{template.path}/{template.name}'
        if template.path == '':
            message = f'Creating {self._runtime.working_directory}/{template.name}'

        Console.spinner(
            message,
            self._create_file,
            file_path,
            template.value,
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

        if schematic in self._schematics:
            s = self._schematics[schematic]
            self._generate(schematic, name, s["Template"])

        else:
            self._help('Usage: cpl generate <schematic> [options]')
            exit()

        Console.write('\n')
