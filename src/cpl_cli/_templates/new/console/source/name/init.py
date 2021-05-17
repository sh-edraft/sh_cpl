import os.path
import textwrap

from cpl.utils.string import String
from cpl_cli._templates.template_file_abc import TemplateFileABC


class MainInitTemplate(TemplateFileABC):

    def __init__(self, name: str, path: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = '__init__.py'
        self._path = os.path.join(path, name)
        self._value = textwrap.dedent("""\
            # imports: 
        """)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def value(self) -> str:
        return self._value
