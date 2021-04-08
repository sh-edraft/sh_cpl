import textwrap

from cpl.utils.string import String
from cpl_cli.templates.template_file_abc import TemplateFileABC


class NameInitTemplate(TemplateFileABC):

    def __init__(self, name: str):
        TemplateFileABC.__init__(self)

        name = String.convert_to_snake_case(name)
        self._name = '__init__.py'
        self._path = f'src/{name}/'
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
