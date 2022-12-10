import importlib
import os
import sys
import textwrap
import traceback

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import WorkspaceSettings
from cpl_cli.configuration.schematic_collection import SchematicCollection
from cpl_cli.helper.dependencies import Dependencies
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.utils.string import String


class GenerateService(CommandABC):

    def __init__(
            self,
            configuration: ConfigurationABC,
            workspace: WorkspaceSettings,
    ):
        """
        Service for the CLI command generate
        :param configuration:
        """
        CommandABC.__init__(self)

        self._config = configuration
        self._workspace = workspace

        self._config = configuration
        self._env = self._config.environment
        self._schematics = {}

        for package_name, version in Dependencies.get_cpl_packages():
            if package_name == 'cpl-cli':
                continue
            package = importlib.import_module(String.convert_to_snake_case(package_name))
            self._read_custom_schematics_from_path(os.path.dirname(package.__file__))

        self._read_custom_schematics_from_path(self._env.working_directory)
        self._read_custom_schematics_from_path(self._env.runtime_directory)

        if len(GenerateSchematicABC.__subclasses__()) == 0:
            Console.error(f'No schematics found in template directory: .cpl')
            sys.exit()

        known_schematics = []
        for schematic in GenerateSchematicABC.__subclasses__():
            if schematic.__name__ in known_schematics:
                Console.error(f'Duplicate of schematic {schematic.__name__} found!')
                sys.exit()

            known_schematics.append(schematic.__name__)
            schematic.register()

        self._schematics = SchematicCollection.get_schematics()

    @property
    def help_message(self) -> str:
        schematics = []
        for schematic in self._schematics:
            aliases = '|'.join(self._schematics[schematic]['Aliases'])
            schematic_str = schematic
            if len(aliases) > 0:
                schematic_str = f'{schematic} ({aliases})'

            schematics.append(schematic_str)
        help_msg = textwrap.dedent("""\
        Generate a file based on schematic.
        Usage: cpl generate <schematic> <name>
        
        Arguments:
            schematic:  The schematic to generate.
            name:       The name of the generated file
            
        Schematics:""")

        for schematic in schematics:
            help_msg += f'\n    {schematic}'
        return help_msg

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

    def _create_init_files(self, file_path: str, template: GenerateSchematicABC, class_name: str, schematic: str, rel_path: str):
        if not os.path.isdir(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
            directory = ''
            for subdir in template.path.split('/'):
                directory = os.path.join(directory, subdir)
                if subdir == 'src':
                    continue

                file = self._schematics['init']['Template'](class_name, 'init', rel_path)
                if os.path.exists(os.path.join(os.path.abspath(directory), file.name)):
                    continue

                Console.spinner(
                    f'Creating {os.path.abspath(directory)}/{file.name}',
                    self._create_file,
                    os.path.join(os.path.abspath(directory), file.name),
                    file.get_code(),
                    text_foreground_color=ForegroundColorEnum.green,
                    spinner_foreground_color=ForegroundColorEnum.cyan
                )

    def _generate(self, schematic: str, name: str, template: type):
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

            if self._workspace is not None and parts[0] in self._workspace.projects:
                rel_path = os.path.join(os.path.dirname(self._workspace.projects[parts[0]]), *parts[1:-1])

        template = template(class_name, String.convert_to_snake_case(schematic), rel_path)

        file_path = os.path.join(self._env.working_directory, template.path, template.name)
        self._create_init_files(file_path, template, class_name, schematic, rel_path)

        if os.path.isfile(file_path):
            Console.error(f'{String.first_to_upper(schematic)} already exists!\n')
            sys.exit()

        message = f'Creating {self._env.working_directory}/{template.path}/{template.name}'
        if template.path == '':
            message = f'Creating {self._env.working_directory}/{template.name}'

        Console.spinner(
            message,
            self._create_file,
            file_path,
            template.get_code(),
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )

    @staticmethod
    def _read_custom_schematics_from_path(path: str):
        if not os.path.exists(os.path.join(path, '.cpl')):
            return

        sys.path.insert(0, os.path.join(path, '.cpl'))
        for r, d, f in os.walk(os.path.join(path, '.cpl')):
            for file in f:
                if not file.startswith('schematic_') or not file.endswith('.py'):
                    continue

                try:
                    exec(open(os.path.join(r, file), 'r').read())
                except Exception as e:
                    Console.error(str(e), traceback.format_exc())
                    sys.exit(-1)

    def _get_schematic_by_alias(self, schematic: str) -> str:
        for key in self._schematics:
            if schematic in self._schematics[key]['Aliases']:
                return key

        return schematic

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        schematic = None
        value = None
        for s in self._schematics:
            value = self._config.get_configuration(s)
            if value is not None:
                schematic = s
                break

        schematic_by_alias = self._get_schematic_by_alias(args[0])
        if schematic is None and len(args) >= 1 and (args[0] in self._schematics or schematic_by_alias != args[0]):
            schematic = schematic_by_alias
            self._config.add_configuration(schematic, args[1])
            value = args[1]

        if schematic is None:
            Console.error(f'Schematic not found')
            Console.write_line(self.help_message)
            sys.exit()

        name = value
        if name is None:
            name = Console.read(f'Name for the {args[0]}: ')

        if schematic in self._schematics:
            s = self._schematics[schematic]
            self._generate(schematic, name, s["Template"])

        else:
            self._help('Usage: cpl generate <schematic> [options]')
            Console.write_line()
            sys.exit()
