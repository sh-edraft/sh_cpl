import os
import sys
import textwrap
from collections import Callable

from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.console.console import Console
from cpl_core.utils.string import String
from cpl_cli.command_abc import CommandABC
from cpl_cli._templates.generate.init_template import InitTemplate
from cpl_cli._templates.generate.abc_template import ABCTemplate
from cpl_cli._templates.generate.class_template import ClassTemplate
from cpl_cli._templates.generate.configmodel_template import ConfigModelTemplate
from cpl_cli._templates.generate.enum_template import EnumTemplate
from cpl_cli._templates.generate.service_template import ServiceTemplate
from cpl_cli._templates.generate.thread_template import ThreadTemplate
from cpl_cli._templates.template_file_abc import TemplateFileABC


class GenerateService(CommandABC):

    def __init__(self, configuration: ConfigurationABC):
        """
        Service for the CLI command generate
        :param configuration:
        """
        CommandABC.__init__(self)

        self._schematics = {
            "abc": {
                "Upper": "ABC",
                "Template": ABCTemplate
            },
            "class": {
                "Upper": "",
                "Template": ClassTemplate
            },
            "enum": {
                "Upper": "Enum",
                "Template": EnumTemplate
            },
            "service": {
                "Upper": "Service",
                "Template": ServiceTemplate
            },
            "settings": {
                "Upper": "Settings",
                "Template": ConfigModelTemplate
            },
            "thread": {
                "Upper": "Thread",
                "Template": ThreadTemplate
            }
        }

        self._config = configuration
        self._env = self._config.environment

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Generate a file based on schematic.
        Usage: cpl generate <schematic> <name>
        
        Arguments:
            schematic:  The schematic to generate.
            name:       The name of the generated file
            
        Schematics:
            abc
            class
            enum
            service
            settings
            thread
        """)

    @staticmethod
    def _help(message: str):
        """
        Internal help output
        :param message:
        :return:
        """
        Console.error(message)

        schematics = [
            'abc (a|A)',
            'class (c|C)',
            'enum (e|E)',
            'service (s|S)',
            'settings (st|ST)'
        ]
        Console.write_line('Available Schematics:')
        for name in schematics:
            Console.write(f'\n\t{name} ')

    @staticmethod
    def _create_file(file_path: str, value: str):
        """
        Creates the given file with content
        :param file_path:
        :param value:
        :return:
        """
        with open(file_path, 'w') as template:
            template.write(value)
            template.close()

    def _generate(self, schematic: str, name: str, template: Callable[TemplateFileABC]):
        """
        Generates files by given schematic, name and template
        :param schematic:
        :param name:
        :param template:
        :return:
        """
        class_name = name
        rel_path = ''
        if '/' in name:
            parts = name.split('/')
            rel_path = '/'.join(parts[:-1])
            class_name = parts[len(parts) - 1]

        if 'src' not in rel_path:
            rel_path = f'src/{rel_path}'

        template = template(class_name, schematic, self._schematics[schematic]["Upper"], rel_path)

        file_path = os.path.join(self._env.working_directory, template.path, template.name)
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
            directory = ''
            for subdir in template.path.split('/'):
                directory = os.path.join(directory, subdir)
                if subdir != 'src':
                    file = InitTemplate(class_name, schematic, self._schematics[schematic]["Upper"], rel_path)
                    Console.spinner(
                        f'Creating {os.path.abspath(directory)}/{file.name}',
                        self._create_file,
                        os.path.join(os.path.abspath(directory), file.name),
                        file.value,
                        text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.cyan
                    )

        if os.path.isfile(file_path):
            Console.error(f'{String.first_to_upper(schematic)} already exists!')
            sys.exit()

        message = f'Creating {self._env.working_directory}/{template.path}/{template.name}'
        if template.path == '':
            message = f'Creating {self._env.working_directory}/{template.name}'

        Console.spinner(
            message,
            self._create_file,
            file_path,
            template.value,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            self._help('Usage: cpl generate <schematic> [options]')
            sys.exit()

        schematic = args[0]
        name = self._config.get_configuration(schematic)
        if name is None:
            name = Console.read(f'Name for the {args[0]}: ')

        if schematic in self._schematics:
            s = self._schematics[schematic]
            self._generate(schematic, name, s["Template"])

        else:
            self._help('Usage: cpl generate <schematic> [options]')
            sys.exit()
