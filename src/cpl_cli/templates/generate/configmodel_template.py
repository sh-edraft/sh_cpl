import textwrap
from string import Template

from cpl.utils.string import String
from cpl_cli.templates.template_file_abc import TemplateFileABC


class ConfigModelTemplate(TemplateFileABC):

    def __init__(self, name: str, schematic: str, schematic_upper: str, path: str):
        TemplateFileABC.__init__(self)

        self._name = f'{String.convert_to_snake_case(name)}.{schematic}.py'
        self._class_name = f'{String.first_to_upper(name)}{schematic_upper}'
        self._path = path
        self._value = textwrap.dedent("""\
        import traceback

        from cpl.configuration.configuration_model_abc import ConfigurationModelABC
        from cpl.console import Console
        
        
        class $Name(ConfigurationModelABC):
        
            def __init__(self):
                ConfigurationModelABC.__init__(self)
        
                self._atr = ''
        
            @property
            def atr(self) -> str:
                return self._atr
        
            def from_dict(self, settings: dict):
                try:
                    self._atr = settings['atr']
                except Exception as e:
                    Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {self.__name__} settings')
                    Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
        """)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> str:
        return Template(self._value).substitute(
            Name=self._class_name
        )
