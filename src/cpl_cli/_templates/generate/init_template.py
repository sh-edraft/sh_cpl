import textwrap
from string import Template

from cpl.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class InitTemplate(TemplateFileABC):

    def __init__(self, name: str, schematic: str, schematic_upper: str, path: str):
        TemplateFileABC.__init__(self)

        self._name = f'__init__.py'
        self._class_name = f'{String.first_to_upper(name)}{schematic_upper}'
        self._path = path
        self._value = textwrap.dedent("""\
        # imports
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
