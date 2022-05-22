import textwrap
from string import Template

from cpl_core.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class PipeTemplate(TemplateFileABC):

    def __init__(self, name: str, schematic: str, schematic_upper: str, path: str):
        TemplateFileABC.__init__(self)

        self._name = f'{String.convert_to_snake_case(name)}_{schematic}.py'
        self._class_name = f'{String.first_to_upper(name)}{schematic_upper}'
        self._path = path
        self._value = textwrap.dedent("""\
        from cpl_core.pipe import PipeABC
        
        
        class $Name(PipeABC):

            def __init__(self): pass
        
            def transform(self, value: any, *args):
                return value
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
